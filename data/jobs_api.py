import flask
from flask import jsonify
from data import db_session
from data.jobs import Jobs

blueprint = flask.Blueprint('jobs_api', __name__,
                            template_folder='templates')


@blueprint.route('/api/jobs/<int:jobs_id>', methods=['GET'])
def get_one_job(job_id):
    session = db_session.create_session()
    job = session.query(Jobs).get(job_id)
    if not job and job_id:
        return jsonify({'error'.upper(): 'Ты id ошибся'})
    jobs = session.query(Jobs).all()
    if not jobs:
        return jsonify({'error'.upper(): 'Ты id ошибся'})

    js = jsonify(
        {
            'job': job.to_dict(only=('id', 'team_leader', 'job', 'work_size', 'collaborators',
                                     'start_date', 'end_date', 'is_finished', 'category'))
        }
    )
    if not js:
        return
