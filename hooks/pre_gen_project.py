#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2018 - 2023 Karlsruhe Institute of Technology - Scientific Computing Center
# This code is distributed under the MIT License
# Please, see the LICENSE file

"""
    Pre-hook script
    1. Check that {{ cookiecutter.git_base_url}} is a valid URL
    2. Check that {{ cookiecutter.__app_name }}:
      a. is not too short (has to be more than one character)
      b. has characters valid for python
"""

import logging
import re
import sys
from urllib.parse import urlparse

import requests
import requests.exceptions

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
FOLDER_REGEX = r"^[a-zA-Z0-9_-]+$"
MODULE_REGEX = r"^[_a-zA-Z][_a-zA-Z0-9]+$"
EMAIL_REGEX = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
APP_VERSION_REGEX = r"^\d+\.\d+\.\d+$"
DOCKER_HUB_API = "https://registry.hub.docker.com/v2"
REQ_TIMEOUT = 1000  # Milliseconds


# -----------------------------------------------------------------------------
def validate_git_base_url():
    """Validate git_base_url"""
    git_base_url = "{{ cookiecutter.git_base_url }}"
    parsed_url = urlparse(url=git_base_url)
    if not bool(parsed_url.scheme and parsed_url.netloc):
        e_message = f"Invalid git_base_url ({git_base_url})"
        logging.error(e_message)
        raise ValueError(e_message)


# -----------------------------------------------------------------------------
def validate_project_name():
    """Validate project_name"""
    project_name = "{{ cookiecutter.project_name }}"
    e_message = []
    if len(project_name) < 2:
        e_message = f"Invalid project name ({project_name}), length < 2 characters"
        logging.error(e_message)
        raise ValueError(e_message)
    if len(project_name.split(" ")) > 4:
        e_message = f"Invalid project name ({project_name}), length > 4 words)"
        logging.error(e_message)
        raise ValueError(e_message)


# repo_name and app_name are derived automatically in cookiecutter.json,
# nevertheless, let's check them here


def validate_repo_name():
    """Validate repo_name"""
    repo_name = "{{ cookiecutter.__repo_name }}"
    if not re.match(FOLDER_REGEX, repo_name):
        e_message = f"Invalid characters in repo_name ({repo_name})"
        logging.error(e_message)
        raise ValueError(e_message)


def validate_app_name():
    """Validate app_name"""
    app_name = "{{ cookiecutter.__app_name }}"
    if not re.match(MODULE_REGEX, app_name):
        e_message = f"Invalid package name ({app_name})"
        logging.error(e_message)
        raise ValueError(e_message)


# -----------------------------------------------------------------------------
def validate_authors():
    """Validate author_emails and author_names"""
    author_emails = "{{ cookiecutter.author_email }}".split(",")
    for email in author_emails:
        if not re.match(EMAIL_REGEX, email.strip()):
            e_message = f"Invalid author_email ({email})"
            logging.error(e_message)
            raise ValueError(e_message)
    author_names = "{{ cookiecutter.author_name }}".split(",")
    lens = n_authors, n_emails = len(author_names), len(author_emails)
    if n_emails != n_authors:
        e_message = f"Authors ({n_authors}) not matching number of emails ({n_emails})"
        logging.error(e_message)
        raise ValueError(e_message)


# -----------------------------------------------------------------------------
def validate_app_version():
    """Validate app_version"""
    app_version = "{{ cookiecutter.app_version }}"
    if not re.match(APP_VERSION_REGEX, app_version):
        e_message = f"Invalid app_version ({app_version})"
        logging.error(e_message)
        raise ValueError(e_message)


# -----------------------------------------------------------------------------
def validate_docker_image():
    """Validate docker image in docker hub"""
    # Construct the URL for Docker Hub API v2
    image = "{{ cookiecutter.docker_baseimage }}"
    cpu_tag = "{{ cookiecutter.baseimage_tag }}"
    gpu_tag = "{{ cookiecutter.baseimage_gpu_tag }}"

    cpu_image_url = f"{DOCKER_HUB_API}/repositories/{image}/tags/{cpu_tag}"
    try:
        response = requests.get(cpu_image_url, timeout=REQ_TIMEOUT)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        e_message = f"Invalid docker image {image}:{cpu_tag}\n{err}"
        logging.error(e_message)
        raise ValueError(e_message)
    except requests.exceptions.Timeout:
        logging.warning(f"Timeout for {cpu_image_url}")
        pass  # In case of network fail, continue

    gpu_image_url = f"{DOCKER_HUB_API}/repositories/{image}/tags/{gpu_tag}"
    try:
        response = requests.get(gpu_image_url, timeout=REQ_TIMEOUT)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        e_message = f"Invalid docker image {image}:{cpu_tag}\n{err}"
        logging.error(e_message)
        raise ValueError(e_message)
    except requests.exceptions.Timeout:
        logging.warning(f"Timeout for {gpu_image_url}")
        pass  # In case of network fail, continue


# -----------------------------------------------------------------------------
# Run all validations, exit with error if any
# init error_messages
error = False
error_messages = []
validations = [
    validate_git_base_url,
    validate_project_name,
    validate_repo_name,
    validate_app_name,
    validate_authors,
    validate_app_version,
    validate_docker_image,
]

# allow to run all validations
for fn in validations:
    try:
        fn()
    except ValueError as err:
        error_messages.append(err.args[0])
        error = True

# if any error, raise SystemExit(1)
if error:
    # e_message = "; ".join(error_messages)
    # logging.error(e_message, exc_info=True)
    raise SystemExit(1)
