from flask import (Blueprint, request, render_template, flash, session, redirect, url_for, jsonify,
                   request, make_response, Response)


shortener_module = Blueprint('', __name__, url_prefix='/')

