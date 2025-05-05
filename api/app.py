# Import dependencies
from sqlalchemy import func, select
from sqlalchemy.orm import joinedload
from flask import Flask, jsonify, request, render_template, abort
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix
import datetime as dt

# and subpackages
from core import Database, get_settings, get_session_factory, forge_json
from schemas import Boroughs, Cuisines, Restaurants

# Create Database object for easy connection
cfg = get_settings()
dbapi = Database(get_session_factory())


#################################################
# Flask Setup
#################################################
app = Flask(__name__, template_folder = cfg.templates)
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto = 1, x_host = 1)
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
    return render_template('home.html')

# Endpoint for interactive heat map
@app.route(map_node)
def api_map():
    '''Endpoint for restaurant markers with details.

    Returns:
        flask.Response: JSON response containing endpoint data.
    '''
    stmt = select(Restaurants).options(joinedload(Restaurants.borough), joinedload(Restaurants.cuisine))
    results = dbapi.execute_query(stmt)
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


# Endpoint for bar chart
@app.route(topCuisines_node)
def api_topCuisines():
    '''Endpoint for aggregated counts of cuisines in a given borough.

    Query Parameters:
        borough (str): Name of the borough to filter cuisines.

    Returns:
        flask.Response: JSON response containing endpoint data.
    '''
    boro_param = request.args.get('borough')
    if boro_param not in C.REF_SEQS['BOROUGHS']:
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
    with dbapi.get_session() as session:
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


# Endpoint for total pie chart
@app.route(cuisineDist_node)
def api_cuisine_pie():
    '''Endpoint for the percentage distribution of different ethnic cuisines.

    Returns:
        flask.Response: JSON response containing endpoint data.
    '''
    with dbapi.get_session() as session:    
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


@app.route(boroughSummary_node)
def api_borough_summary():
    '''Endpoint for borough summaries.

    Returns:
        flask.response: JSON response containing endpoint data.
    '''
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
    with dbapi.get_session() as session:
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


# EOF

if __name__ == '__main__':
    print('This module is intended to be imported, not run directly.')