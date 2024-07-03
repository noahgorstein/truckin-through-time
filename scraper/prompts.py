PARSE_CONCERT_PROMPT = """
Given the following Grateful Dead concert information, return to me the following information
in a JSON object. Venue, City, State, Country, Date (in format MM/DD/YYYY).
- If country information is not there, use your knowledge based on the concert information to fill it in.
- If the concert does not place in the USA, return null for state and just provide the country.

Do not return to me any additional information about what you returned. Only return the JSON object.

Example concert information:

The Spectrum, Philadelphia, PA (4/22/77)

Example JSON Object:

{{
  "venue": "The Spectrum",
  "city": "Philadelphia",
  "state": "PA",
  "country": "USA",
  "date": "04/22/1977"
}}

This is the concert you need to parse and return JSON for:

{concert}
"""


PARSE_SETLIST_PROMPT = """
Given the following text file representing a setlist from a Grateful dead concert, return to the
me the following information in a JSON object.
- List of songs played and any special notes about the setlist.
    - Use your own judgement to create the notes. They should be concise.
    - A song should be represented with the following information: title, order played, and whether it was transition into another song.
    - Please correct any typos you may find and remove any extraneous information.

Example setlist:

NBC Studios, New York, NY (9/17/87)

Comments: David Letterman

Good Lovin'
All Along the Watchtower
Walkin' the Dog
Tore Up Over You
Kansas City

Masterpiece

Example JSON Object:

{{
  "songs": [
    {{
      "title": "Good Lovin'",
      "order": 1,
      "transition": false
    }},
    {{
      "title": "All Along the Watchtower",
      "order": 2,
      "transition": false
    }},
    {{
      "title": "Walking the Dog",
      "order": 3,
      "transition": false
    }},
    {{
      "title": "Tore Up Over You",
      "order": 4,
      "transition": false
    }},
    {{
      "title": "Kansas City",
      "order": 5,
      "transition": false
    }},
    {{
      "title": "Masterpiece",
      "order": 6,
      "transition": false
    }}
  ],
  "notes": "Played on David Letterman Show"
}}

Here is the setlist for you to parse:

{setlist}


This is the end of the setlist. Please do not return to me any additional information about what you returned. Only return the JSON object.
"""
