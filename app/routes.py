import logging

import flask
from flask import Response
import json
from app.profile_services import get_profiles

app = flask.Flask("user_profiles_api")
logger = flask.logging.create_logger(app)
logger.setLevel(logging.INFO)


@app.route("/health-check", methods=["GET"])
def health_check():
    """
    Endpoint to health check API
    """
    app.logger.info("Health Check!")
    return Response("All Good!", status=200)


"""Example endpoint To test: curl http://localhost:5000/profiles/mailchimp/mailchimp"""
@app.route('/profiles/<github_org>/<bitbucket_team>', methods=["GET"])
def profile(github_org, bitbucket_team):
# try:
    # github_org = "mailchimp"
    # bitbucket_team = "mailchimp"
    # github_token = None

    profile_data = get_profiles(
        github_org,
        bitbucket_team
    )
    response_data = {
        'status': 'success',
        'data': profile_data['data'],
        'sources': profile_data['sources']
    }
    return Response(
        json.dumps(response_data),
        status=200,
        mimetype='application/json'
    )
