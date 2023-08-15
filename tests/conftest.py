import pytest
import pandas as pd


@pytest.fixture
def make_parse_dict():
    return {
        "MatchedObjectId": "739502000",
        "MatchedObjectDescriptor": {
            "PositionID": "DE-12055252-23-RBS",
            "PositionTitle": "DISTINGUISHED SCIENTIST/ENGINEER FOR NAVAL DATA SCIENCES",
            "PositionURI": "https://www.usajobs.gov:443/GetJob/ViewDetails/739502000",
            "ApplyURI": [
                "https://www.usajobs.gov:443/GetJob/ViewDetails/739502000?PostingChannelID="
            ],
            "PositionLocationDisplay": "Dahlgren, Virginia",
            "PositionLocation": [
                {
                    "LocationName": "Dahlgren, Virginia",
                    "CountryCode": "United States",
                    "CountrySubDivisionCode": "Virginia",
                    "CityName": "Dahlgren, Virginia",
                    "Longitude": -77.0468,
                    "Latitude": 38.331,
                }
            ],
            "OrganizationName": "Naval Sea Systems Command",
            "DepartmentName": "Department of the Navy",
            "JobGrade": [{"Code": "ND"}],
            "PositionSchedule": [{"Name": "", "Code": "1"}],
            "PositionOfferingType": [{"Name": "", "Code": "15317"}],
            "PositionRemuneration": [
                {
                    "MinimumRange": "186841.0",
                    "MaximumRange": "195000.0",
                    "RateIntervalCode": "PA",
                    "Description": "Per Year",
                }
            ],
            "PositionStartDate": "2023-07-26T00:00:00.0000",
            "PositionEndDate": "2023-08-24T23:59:59.9970",
            "PublicationStartDate": "2023-07-26T00:00:00.0000",
            "ApplicationCloseDate": "2023-08-24T23:59:59.9970",
            "PositionFormattedDescription": [
                {
                    "Label": "Dynamic Teaser",
                    "LabelDescription": "Hit highlighting for keyword searches.",
                }
            ],
            "UserArea": {
                "Details": {
                    "JobSummary": "You will serve as the Distinguished Scientist or Engineer of Naval Data Sciences of Naval Surface Warfare Center Dahlgren Division (NSWCDD). THIS IS A DIRECT HIRE ANNOUNCEMENT (see the Additional Information section for further information regarding this Direct Hire Authority).",
                    "WhoMayApply": {"Name": "", "Code": ""},
                    "LowGrade": "6",
                    "HighGrade": "6",
                    "PromotionPotential": "None",
                    "OrganizationCodes": "DD/NV24",
                    "Relocation": "False",
                    "HiringPath": ["public"],
                    "TravelCode": "1",
                    "ApplyOnlineUrl": "https://apply.usastaffing.gov/Application/Apply",
                    "DetailStatusUrl": "https://apply.usastaffing.gov/Application/ApplicationStatus",
                    "Benefits": "",
                    "BenefitsUrl": "http://www.secnav.navy.mil/donhr/Benefits/Pages/Default.aspx",
                    "BenefitsDisplayDefaultText": True,
                    "KeyRequirements": [],
                    "WithinArea": "False",
                    "CommuteDistance": "0",
                    "ServiceType": "01",
                    "AnnouncementClosingType": "01",
                    "AgencyContactEmail": "usn.seattle-wa.ochrsvdopscenwa.mbx.don-executive-hiring@us.navy.mil",
                    "SecurityClearance": "Sensitive Compartmented Information",
                    "DrugTestRequired": "True",
                    "PositionSensitivitiy": "Special-Sensitive (SS)/High Risk",
                    "AdjudicationType": ["Suitability/Fitness"],
                    "TeleworkEligible": True,
                    "RemoteIndicator": False,
                },
                "IsRadialSearch": False,
            },
        },
        "RelevanceRank": 0,
    }


@pytest.fixture
def make_filter_dict_chicago():
    return {
        "PositionLocationDisplay": "Anywhere in the U.S. (remote job)",
        "PositionLocation": [
            {
                "LocationName": "Wallops Island, Virginia",
                "CountryCode": "United States",
                "CountrySubDivisionCode": "Virginia",
                "CityName": "Wallops Island, Virginia",
                "Longitude": -75.47912,
                "Latitude": 37.844044,
            },
            {
                "LocationName": "Boise, Idaho",
                "CountryCode": "United States",
                "CountrySubDivisionCode": "Idaho",
                "CityName": "Boise, Idaho",
                "Longitude": -116.19341,
                "Latitude": 43.60698,
            },
            {
                "LocationName": "Chicago, Illinois",
                "CountryCode": "United States",
                "CountrySubDivisionCode": "Illinois",
                "CityName": "Chicago, Illinois",
                "Longitude": -87.63241,
                "Latitude": 41.88415,
            },
        ],
    }


@pytest.fixture
def make_filter_dict_no_chicago():
    return {
        "PositionLocationDisplay": "Anywhere in the U.S. (remote job)",
        "PositionLocation": [
            {
                "LocationName": "Wallops Island, Virginia",
                "CountryCode": "United States",
                "CountrySubDivisionCode": "Virginia",
                "CityName": "Wallops Island, Virginia",
                "Longitude": -75.47912,
                "Latitude": 37.844044,
            },
            {
                "LocationName": "Boise, Idaho",
                "CountryCode": "United States",
                "CountrySubDivisionCode": "Idaho",
                "CityName": "Boise, Idaho",
                "Longitude": -116.19341,
                "Latitude": 43.60698,
            },
        ],
    }


@pytest.fixture
def make_dict_num_pages():
    return {
        "LanguageCode": "EN",
        "SearchParameters": {},
        "SearchResult": {
            "SearchResultCount": 25,
            "SearchResultCountAll": 1579,
            "SearchResultItems": [
                {
                    "MatchedObjectId": "740824700",
                    "MatchedObjectDescriptor": {
                        "PositionID": "ST-12073977-23-KFF",
                        "PositionTitle": "ENGINEERING DATA MANAGEMENT SPECIALIST",
                        "PositionURI": "https://www.usajobs.gov:443/GetJob/ViewDetails/740824700",
                        "ApplyURI": [
                            "https://www.usajobs.gov:443/GetJob/ViewDetails/740824700?PostingChannelID="
                        ],
                        "PositionLocationDisplay": "China Lake, California",
                        "PositionLocation": [
                            {
                                "LocationName": "China Lake, California",
                                "CountryCode": "United States",
                                "CountrySubDivisionCode": "California",
                                "CityName": "China Lake, California",
                                "Longitude": -117.67,
                                "Latitude": 35.6506,
                            }
                        ],
                        "OrganizationName": "Naval Air Systems Command",
                    },
                }
            ],
        },
    }
