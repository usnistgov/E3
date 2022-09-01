---
title: "Authentication"
date: 2022-08-30T12:32:14-04:00
draft: true
---

# About

E3 is a REST API for running standards-based, multi-year economic analyses. TODO: add more

## Why

E3 provides a single, proven calculation engine that can be used for a variety of economic tools. This allows
resources and time to be focused on developing higher quality tools instead of re-inventing the economic formulas over
and over.

To that end, E3 is open-soured and an instance is hosted by NIST that can be used free of charge.

# Getting Started

To get started with E3, you can either host your own instance or use the instance hosted by NIST at
[e3.nist.gov](https://e3.nist.gov). Instructions on hosting your own instance are below.

## Self-Hosting E3

TODO

# Authentication

E3 is free to use, however API keys are still required on requests for statistical and
rate-limiting purposes. Getting an API key is simple. First, go to the E3 login page
[e3.nist.gov/login/](https://e3.nist.gov/login/) and login with your username and password, or register if you have
not already done so.

Then under the API key table, click the add button, enter a name for the key, and set an expiration date if desired.
Leaving the expiration date empty will cause the key to never expire.

To use the API key, you must include it as an HTTP header with your request. The headers must have the name
`Authorization` with the value `Api-Key YOUR_KEY_HERE`, replacing `YOUR_KEY_HERE` with your API key. A complete header
would appear something like `Authorization: Api-Key wxyz...`.

# Requests

This guide is intended to explain the general layout of an E3 JSON request. It is not intended to be a guide on how to
structure an economic analysis. For a more in-depth explanation of the economic side of E3, please refer to the
[technical manual](https://nvlpubs.nist.gov/nistpubs/TechnicalNotes/NIST.TN.2225.pdf).

## General Structure

An E3 request has three major parts, the analysis object, the alternative objects, and the BCN objects.

## Analysis Object

The analysis object contains variables that influence the entire analysis. This is where you set which objects you would
like to have outputted, discount rates, the length of the study period, etc.

### Example Analysis Object

```json
{
  "analysisObject": {
    "analysisType": "LCCA",
    "projectType": "Buildings",
    "objToReport": [
      "FlowSummary",
      "MeasureSummary",
      "OptionalSummary"
    ],
    "studyPeriod": 20,
    "baseDate": "2022-01-01",
    "serviceDate": "2022-01-01",
    "timestepVal": "Year",
    "timestepComp": "EndOfYear",
    "outputRealBool": true,
    "interestRate": null,
    "dRateReal": 0.030,
    "dRateNom": null,
    "inflationRate": 0.023,
    "Marr": 0.03,
    "reinvestRate": 0.03,
    "incomeRateFed": null,
    "incomeRateOther": null,
    "location": [
      "United States",
      "DC"
    ],
    "noAlt": 2,
    "baseAlt": 0
  }
}
```

## Alternative Objects

Alternatives are the main objects of comparison in an E3 analysis. For example, if a user wanted to see the return of
investment of installing solar panels they might include a control or business-as-usual alternative with no panel
installation, an alternative with solar panels with up-front payment, and an alternative with solar panels paid by a
loan. In this example those three alternatives would provide a clearer picture of which option will be most economically
viable.

### Example Alternative Objects

```json
{
  "alternativeObjects": [
    {
      "altID": 0,
      "altName": "Alt 0 Conventional",
      "altBCNList": [
        0,
        1,
        2,
        3,
        4
      ],
      "baselineBool": true
    },
    {
      "altID": 1,
      "altName": "Alt 1 High Efficiency",
      "altBCNList": [
        5,
        6,
        7,
        8,
        9
      ],
      "baselineBool": false
    }
  ]
}
```

## BCN Objects

BCN objects are what define the monetary and non-monetary cashflows used in the analysis. BCNs can require a large
amount of configuration and may need to be split into multiple BCNs for some complex scenarios. BCNs can be used in
multiple alternatives in order to reduce writing.

BCNs may also be grouped together with tags for better understanding. For example in our solar panel example, electrical
costs may be grouped together so we can see those costs individually apart from the cost of the solar panels themselves.

### BCN Objects Example

```json
{
  "bcnObjects": [
    {
      "bcnID": 0,
      "altID": [
        0
      ],
      "bcnType": "Cost",
      "bcnSubType": "Direct",
      "bcnName": "HVAC System Conventional",
      "bcnTag": "Initial Investment",
      "initialOcc": 0,
      "bcnRealBool": true,
      "rvBool": false,
      "rvOnly": false,
      "bcnInvestBool": true,
      "bcnLife": 20,
      "recurBool": false,
      "recurInterval": null,
      "recurVarRate": null,
      "recurVarValue": null,
      "recurEndDate": null,
      "valuePerQ": 103000,
      "quant": 1,
      "quantVarRate": null,
      "quantVarValue": null,
      "quantUnit": null
    },
    {
      "bcnID": 1,
      "altID": [
        0
      ],
      "bcnType": "Cost",
      "bcnSubType": "Direct",
      "bcnName": "Fan Replacement",
      "bcnTag": "Replacement Costs",
      "initialOcc": 12,
      "bcnRealBool": true,
      "bcnInvestBool": true,
      "rvBool": false,
      "rvOnly": false,
      "bcnLife": null,
      "recurBool": false,
      "recurInterval": null,
      "recurVarRate": null,
      "recurVarValue": null,
      "recurEndDate": null,
      "valuePerQ": 12000,
      "quant": 1,
      "quantVarRate": null,
      "quantVarValue": null,
      "quantUnit": null
    }
  ]
}
```

# E3 Request Javascript Library

In order to make creating requests easier from web apps, a javascript library that helps with building requests
has been created. The library uses the builder pattern to allow for easy re-using of request components. Additionally 
some values in the request, such as BCN and alternative IDs, will be automatically added and inserted into the
proper locations, can be overridden and set manually, or a mixture of the two.