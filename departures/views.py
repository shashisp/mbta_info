# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.http import JsonResponse
import requests


def get_info_object(data_list, object_id):
	for obj in data_list:
		if obj.get('id') == object_id:
			return obj
	return None


def clean_up_response(data):
	included_info = data.get('included')
	depart_info = data.get('data')
	included_trips = []
	included_stops = []
	included_schedules = []
	final_data = {}
	final_data['departure'] = []
	final_data['arrival'] = []
	cleaned_depart = []
	arrival_info = []

	for i in included_info:
		if i['type'] == 'trip':
			included_trips.append(i)
		elif i['type'] == 'stop':
			included_stops.append(i)
		elif i['type'] == 'schedule':
			included_schedules.append(i)

	for dep in depart_info:
		if dep.get('attributes')['departure_time'] and not dep.get('attributes')['arrival_time']:
			cleaned_depart.append(dep)

	for arr in depart_info:
		if arr.get('attributes')['arrival_time']:
			arrival_info.append(arr)

	if arrival_info:
		for dep in arrival_info:
			status = dep.get('attributes')['status']
			destination = dep.get("relationships")["route"]["data"]["id"]
			stop_id = dep.get('relationships')['stop']['data']['id']
			stop_info = get_info_object(included_stops, stop_id)
			track = stop_info.get('attributes')['platform_code']

			trip_id = dep.get('relationships')['trip']['data']['id']
			trip_info = get_info_object(included_trips, trip_id)
			vehicle = trip_info.get("attributes")["name"]

			schedule_id = dep.get('relationships')['schedule']['data']['id']
			schedule_info = get_info_object(included_schedules, schedule_id)

			departure_time = schedule_info.get("attributes")["arrival_time"]

			if not track:
				track = "TBD"

			response = {
				"carrier": "MBTA",
				"track": track,
				"vehicle": vehicle,
				"arrival_time": departure_time,
				"status": status,
				"destination": destination
			}
			final_data['arrival'].append(response)


	if cleaned_depart:

		for dep in cleaned_depart:
			response = {}
			status = dep.get('attributes')['status']
			destination = dep.get("relationships")["route"]["data"]["id"]
			stop_id = dep.get('relationships')['stop']['data']['id']
			stop_info = get_info_object(included_stops, stop_id)
			track = stop_info.get('attributes')['platform_code']

			trip_id = dep.get('relationships')['trip']['data']['id']
			trip_info = get_info_object(included_trips, trip_id)
			vehicle = trip_info.get("attributes")["name"]

			schedule_id = dep.get('relationships')['schedule']['data']['id']
			schedule_info = get_info_object(included_schedules, schedule_id)

			departure_time = schedule_info.get("attributes")["departure_time"]

			if not track:
				track = "TBD"

			response = {
				"carrier": "MBTA",
				"track": track,
				"vehicle": vehicle,
				"departure_time": departure_time,
				"status": status,
				"destination": destination
			}
			final_data['departure'].append(response)

	return final_data


def data_api(request):
	station = request.GET.get('station')
	# place-sstat, place-north
	url = "https://api-v3.mbta.com/predictions?filter[stop]="+station+"&filter[route_type]=2&include=stop,trip,schedule"
	response = requests.get(url)
	data = response.json()
	data = clean_up_response(data)
	return JsonResponse(data)


class HomePageView(TemplateView):
    template_name = "home.html"





