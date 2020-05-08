from flask import Blueprint, jsonify, request
from data import db_session
from data.jobs import Jobs
import datetime

blueprint = Blueprint('jobs_api', __name__,
                      template_folder='templates')


@blueprint.route('/api/jobs')
def get_jobs():
    session = db_session.create_session()
    jobs = session.query(Jobs).all()
    return jsonify(
        {
            'jobs':
                [item.to_dict(only=('id', 'team_leader', 'job', 'work_size', 'collaborators',
                                    'start_date', 'end_date', 'is_finished'))
                 for item in jobs]
        }
    )


@blueprint.route('/api/jobs/<int:job_id>', methods=['GET'])
def get_one_jobs(job_id):
    session = db_session.create_session()
    job = session.query(Jobs).get(job_id)
    if not job:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'job': job.to_dict(only=('id', 'team_leader', 'job', 'work_size', 'collaborators',
                                     'start_date', 'end_date', 'is_finished'))
        }
    )


@blueprint.route('/api/jobs', methods=['POST'])
def create_job():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['id', 'team_leader', 'job', 'work_size', 'collaborators', 'is_finished']):
        return jsonify({'error': 'Bad request'})
    session = db_session.create_session()
    if session.query(Jobs).get(request.json['id']):
        return jsonify({'error': 'Id already exists'})
    job = Jobs(
        id=request.json['id'],
        team_leader=request.json['team_leader'],
        job=request.json['job'],
        work_size=request.json['work_size'],
        collaborators=request.json['collaborators'],
        start_date=datetime.datetime.now(),
        is_finished=request.json['is_finished']
    )

    session.add(job)
    session.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/<int:job_id>', methods=['GET', 'POST'])
def transform_one_jobs(job_id):
    session = db_session.create_session()
    job = session.query(Jobs).get(job_id)
    if not job:
        return jsonify({'error': 'Not found'})
    for key in ['id', 'team_leader', 'job', 'work_size', 'collaborators', 'is_finished']:
        if key in request.json.keys():
            exec('job.{}="{}"'.format(key, request.json[key]))
    session.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/<int:job_id>', methods=['DELETE'])
def delete_job(job_id):
    session = db_session.create_session()
    job = session.query(Jobs).get(job_id)
    if not job:
        return jsonify({'error': 'Not found'})
    session.delete(job)
    session.commit()
    return jsonify({'success': 'OK'})
