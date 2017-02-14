from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from . import teaching_fellow
from forms import StudentForm, EventForm, CommentForm
from .. import db
from ..models import Student, Event, Attendance

def check_admin():
    """
    Prevent non-admins from accessing the page
    """
    if not current_user.is_admin:
        abort(403)

# Student Views

@teaching_fellow.route('/students', methods=['GET', 'POST'])
@login_required
def list_students():
    """
    List all students
    """
    check_admin()

    students = Student.query.filter(Student.forum==current_user.forum).all()

    return render_template('teaching_fellow/students/students.html',
                           forum=current_user.forum, students=students, title="Students")

@teaching_fellow.route('/students/add', methods=['GET', 'POST'])
@login_required
def add_student():
    """
    Add a student to the database
    """
    check_admin()

    add_student = True

    form = StudentForm()
    if form.validate_on_submit():
        student = Student(name=form.name.data, forum=form.forum.data)
        try:
            # add student to the database
            db.session.add(student)
            db.session.commit()
            flash('You have successfully added a new student.')
        except:
            # in case student name already exists, FIX LATER
            flash('Error: student name already exists.')

        # redirect to students page
        return redirect(url_for('teaching_fellow.list_students'))

    # load student template
    return render_template('teaching_fellow/students/student.html', action="Add",
                           add_student=add_student, form=form,
                           title="Add Student")

@teaching_fellow.route('/students/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_student(id):
    """
    Edit a student
    """
    check_admin()

    add_student = False

    student = Student.query.get_or_404(id)
    form = StudentForm(obj=student)
    if form.validate_on_submit():
        student.name = form.name.data
        student.forum = form.forum.data
        db.session.commit()
        flash('You have successfully edited the student.')

        # redirect to the students page
        return redirect(url_for('teaching_fellow.list_students'))

    form.name.data = student.name
    form.forum.data = student.forum
    return render_template('teaching_fellow/students/student.html', action="Edit",
                           add_student=add_student, form=form,
                           student=student, title="Edit Student")

@teaching_fellow.route('/students/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_student(id):
    """
    Delete a student from the database
    """
    check_admin()

    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    flash('You have successfully deleted the student.')

    # redirect to the student page
    return redirect(url_for('student.list_students'))

# Events view
@teaching_fellow.route('/events', methods=['GET', 'POST'])
@login_required
def list_events():
    """
    List all events
    """
    check_admin()

    events = Event.query.all()

    return render_template('teaching_fellow/events/events.html',
                           events=events, title="Events")

@teaching_fellow.route('/events/add', methods=['GET', 'POST'])
@login_required
def add_event():
    """
    Add a event to the database
    """
    check_admin()
    add_event = True
    form = EventForm()
    if form.validate_on_submit():
        event = Event(event_name=form.event_name.data, event_description=form.event_description.data,
                      event_date=form.event_date.data)
        try:
            # Create an Attendance object for every student
            # and add them to event
            for student in Student.query.filter(Student.forum==current_user.forum).all():
                attendance = Attendance(TF_comment="", is_attended=False)
                attendance.student = student
                event.attendance.append(attendance)

            db.session.add(event)
            db.session.commit()
            flash('You have successfully added a new event.')
        except:
            flash('Error: can not add event.')

        # redirect to events page
        return redirect(url_for('teaching_fellow.list_events'))

    # load student template
    return render_template('teaching_fellow/events/event.html', action="Add",
                           add_event=add_event, form=form,
                           title="Add Event")

@teaching_fellow.route('/events/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_event(id):
    """
    Edit an event
    """
    check_admin()

    add_event = False

    event = Event.query.get_or_404(id)
    form = EventForm(obj=event)
    if form.validate_on_submit():
        event.event_name = form.event_name.data
        db.session.commit()
        flash('You have successfully edited the event.')

        # redirect to the events page
        return redirect(url_for('teaching_fellow.list_events'))

    form.event_name.data = event.event_name
    return render_template('teaching_fellow/events/event.html', action="Edit",
                           add_event=add_event, form=form,
                           event=event, title="Edit Event")

@teaching_fellow.route('/events/detail/<int:id>', methods=['GET', 'POST'])
@login_required
def detail_event(id):
    check_admin()

    event = Event.query.get_or_404(id)
    forum_attendance = []

    for attendance in event.attendance:
        if attendance.student.forum == current_user.forum:
            forum_attendance.append(attendance)

    # No need for forms
    return render_template('teaching_fellow/events/comments.html', event=event, forum_attendance=forum_attendance)

@teaching_fellow.route('/events/comment/<int:event_id>/<int:student_id>', methods=['GET', 'POST'])
@login_required
def comment(event_id, student_id):
    check_admin()

    attendance = Attendance.query.get([event_id, student_id])

    form = CommentForm(obj=attendance)
    if form.validate_on_submit():
        attendance.is_attended = form.is_attended.data
        attendance.TF_comment = form.TF_comment.data
        db.session.commit()
        flash('You have successfully commented this awesome student.')

        # redirect to the events page
        return redirect(url_for('teaching_fellow.detail_event', id=event_id))

    form.is_attended.data = attendance.is_attended
    form.TF_comment.data = attendance.TF_comment

    return render_template('teaching_fellow/events/comment.html', form=form,
                           name = attendance.student.name, title=attendance.student.name)


@teaching_fellow.route('/events/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_event(id):
    """
    Delete a event from the database
    """
    check_admin()

    event = Event.query.get_or_404(id)
    db.session.delete(event)
    db.session.commit()
    flash('You have successfully deleted the event.')

    # redirect to the student page
    return redirect(url_for('teaching_fellow.list_events'))


