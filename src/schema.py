# coding=utf-8
"""
SCHEMA for validating request and response
"""
from marshmallow import fields, Schema


class RegionSchema(Schema):
    """
    Standardize region request
    """
    name = fields.String(allow_none=True)
    avgAge = fields.Float(required=True, allow_none=False)
    avgDailyIncomeInUSD = fields.Float(required=True, allow_none=False)
    avgDailyIncomePopulation = fields.Float(required=True, allow_none=False)


class CovidRequestSchema(Schema):
    """
    AfricaTalkingResponseSchema Schema
    """

    region = fields.Nested(RegionSchema, required=True, allow_none=False)
    periodType = fields.String(required=True, allow_none=False)
    timeToElapse = fields.Integer(required=True, allow_none=False)
    reportedCases = fields.Integer(required=True, allow_none=False)
    population = fields.Integer(required=True, allow_none=False)
    totalHospitalBeds = fields.Integer(required=True, allow_none=False)
    cache_type = fields.String()


class CovidResponseSchema(Schema):
    """
    AfricaTalkingResponseSchema Schema
    """
    data = fields.Nested(CovidRequestSchema)
    impact = fields.Dict()
    severeImpact = fields.Dict()
    response = fields.String(allow_none=True)  # this here for xml
