# Import dependencies
import datetime as dt
from sqlalchemy import func, select
from sqlalchemy.orm import joinedload
from flask import Flask, jsonify, request, render_template, abort
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix

# Import subpackage dependencies
from Core.database import Restaurants, Boroughs, Cuisines, get_session, execute_query
from .backend import forge_json

# Import config file
import config as C

# Bring in custom logger
from Core.log_config import init_log
log = init_log(__name__)


#################################################
# Flask Setup
#################################################
log.debug('Initializing Flask App with template folder.')
app = Flask(__name__, template_folder = C.TEMPLATE_DIR)
log.debug('Setting ProxyFix for WSGI App.')
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto = 1, x_host = 1)
log.debug('Enabling CORS.')
CORS(app)
app.json.sort_keys = False
app.url_map.strict_slashes = False

# Endpoint Declarations
map_node = '/api/v1.0/map/'
topCuisines_node = '/api/v1.0/top-cuisines/'
cuisineDist_node = '/api/v1.0/cuisine-distributions/'
boroughSummary_node = '/api/v1.0/borough-summaries/'


#################################################
# Flask Endpoints
#################################################

# Endpoint for home
@app.route('/')
def home():
    '''Home endpoint for the API.

    Returns:
        str: HTML content for the home page.
    '''
    try:
        log.debug('Rendering home.html template.')
        return render_template('home.html')
    except Exception:
        log.critical('Could not render home template.', exc_info = True)
        raise

# Endpoint for interactive heat map
@app.route(map_node)
def api_map():
    '''Endpoint for restaurant markers with details.

    Returns:
        flask.Response: JSON response containing endpoint data.
    '''
    try:
        stmt = select(Restaurants).options(joinedload(Restaurants.borough), joinedload(Restaurants.cuisine))
        log.debug('Executing map_node query.')
        results = execute_query(stmt)
        data = [
            {
                'id': r.id,
                'name': r.name,
                'lat': r.lat,
                'lng': r.lng,
                'borough': r.borough.borough,
                'cuisine': r.cuisine.cuisine,
                'inspection_date': dt.date.isoformat(r.inspection_date)
            }
        for r in results]
        desc = 'Retrieves restaurant details for interactive heat map.'
        data_nest = forge_json(map_node, data, desc)
        return jsonify(data_nest)
    except Exception:
        log.critical('Could not execute map_node query.', exc_info = True)
        raise


# Endpoint for bar chart
@app.route(topCuisines_node)
def api_topCuisines():
    '''Endpoint for aggregated counts of cuisines in a given borough.

    Query Parameters:
        borough (str): Name of the borough to filter cuisines.

    Returns:
        flask.Response: JSON response containing endpoint data.
    '''
    try:
        boro_param = request.args.get('borough')
        if boro_param not in C.REF_SEQS['BOROUGHS']:
            log.warning(f'Invalid request parameter: {boro_param}')
            abort(400, description = 'Invalid borough name.')
        counts = func.count(Restaurants.id)
        stmt = (
            select(
                Cuisines.cuisine
                ,counts.label('count')
            ).join(
                Restaurants
            ).join(
                Boroughs
            ).where(
                Boroughs.borough == boro_param
            ).group_by(
                Cuisines.cuisine
            ).order_by(
                counts.desc()
            )
        )
        with get_session() as session:
            results = session.execute(stmt)
            data = [
                {
                    'cuisine': r.cuisine,
                    'count': r.count
                } 
                for r in results]
        desc = 'Retrieves aggregated counts for cuisines in given borough.'
        params = {'borough': boro_param}
        data_nest = forge_json(topCuisines_node, data, desc, params)
        return jsonify(data_nest)
    except Exception:
        log.critical('Could not execute topCuisines_node query.', exc_info = True)
        raise


# Endpoint for total pie chart
@app.route(cuisineDist_node)
def api_cuisine_pie():
    '''Endpoint for the percentage distribution of different ethnic cuisines.

    Returns:
        flask.Response: JSON response containing endpoint data.
    '''
    try:
        with get_session() as session:    
            stmt_total = select(func.count(Restaurants.id))
            total = session.scalar(stmt_total)
            stmt = (
                select(
                    Cuisines.cuisine
                    ,func.count(Restaurants.id).label('count')
                ).join(
                    Restaurants
                ).group_by(
                    Cuisines.cuisine
                )
            )
            results = session.execute(stmt)
            data = [
                {
                    'cuisine': r.cuisine
                    ,'count': r.count
                    ,'percent': (r.count / total * 100)
                }
            for r in results]
        desc = 'Retrieves percent distribution of all cuisines across NYC.'
        data_nest = forge_json(cuisineDist_node, data, desc)
        return jsonify(data_nest)
    except Exception:
        log.critical('Could not execute cuisineDist_node query.', exc_info = True)
        raise


@app.route(boroughSummary_node)
def api_borough_summary():
    '''Endpoint for borough summaries.

    Returns:
        flask.response: JSON response containing endpoint data.
    '''
    try:
        stmt = (
            select(
                Boroughs.borough
                ,func.count(Restaurants.id).label('restaurant_count')
                ,Boroughs.population
            ).join(
                Restaurants
            ).group_by(
                Boroughs.borough
            )
        )
        with get_session() as session:
            results = session.execute(stmt)
            data = [
                {
                    'borough': r.borough
                    ,'restaurant_count': r.restaurant_count
                    ,'population': r.population
                }
            for r in results]
        desc = 'Retrieves summary statistics per each borough.'
        data_nest = forge_json(boroughSummary_node, data, desc)
        return jsonify(data_nest)
    except Exception:
        log.critical('Could not execute query for boroughSummary_node.', exc_info = True)
        raise



if __name__ == '__main__':
    print('This module is intended to be imported, not run directly.')