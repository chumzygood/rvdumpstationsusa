# Additional-source check — November 10, 2026 (EST)

Added twelve properties, all with location-specific official evidence:
- Six USACE campgrounds: Cedar Ridge, Live Oak Ridge, Westcliff and White Flint at Belton Lake; Cranes Mill and Potters Creek at Canyon Lake.
- Three Love's: Ranger #270, Baird #610, Sweetwater #475.
- Three TA: Rockwall #0049, Ganado #0231, Dallas South #0150.

USACE has confirmed park/lake identity and dump amenities but no verified property street addresses in the checked descriptions. Those addresses remain unset; city browse labels explicitly say lake area, and structured data omits unsupported street/locality/postcode. Westcliff and White Flint winter-closure warnings are prominent. The dump service is not advertised as currently open merely because a boat ramp remains open.

Additional checked candidates, deliberately not added:
- TxDOT: https://www.txdot.gov/discover/rest-areas-travel-information-centers/safety-rest-area-list.html — no dump-station confirmation found in the official rest-area list inspected. Third-party reports at Sutton/Kerr/Wichita are leads only, not evidence. This does not assert that no Texas rest area has a dump station.
- Buc-ee's: https://buc-ees.com/locations/ — no location-specific RV dump confirmation found. No Buc-ee's stations added; no blanket absence claim.
- Pilot Flying J: legacy location URLs are changing. The current official Anthony #724 page https://pilotcompany.com/locations/us/tx/anthony/3001-mountain-pass-blvd showed "Temporarily Closed" and no RV dump amenity in its extracted location text. An RV-dump label occurred in raw page scripts but was not confidently bound to that open location, so it was not sufficient to add. Old Orange and Baytown address URLs returned 404. No Pilot stations added from third-party listings or generic nationwide service claims.
- Love's Dallas #294 official current page did not show the sought dump-service confirmation in the inspected amenities; not added despite third-party leads.

Operator-listed does not mean open to non-guests, free, 24-hour, potable-water-equipped or big-rig-safe. Unconfirmed fields stay unknown. All listed properties have official source URLs and a November 10, 2026 source-check date.

# Additional-source check — November 11, 2026 (EST), local only (not pushed)

Added six USACE Fort Worth District campgrounds, each with a location-specific dump-station sentence on the official Corps parks page (direct fetch, snapshot + sha256 in research/usace-<lake>.txt):
- Stillhouse Hollow Lake: Dana Peak Park, Union Grove Park — https://www.swf-wc.usace.army.mil/stillhouse/Recreation/Parks/Corpsparks.shtml
- Lake Georgetown: Cedar Breaks Park, Jim Hogg Park (entry requires pass/online payment/reservation) — https://www.swf-wc.usace.army.mil/georgetown/Recreation/Parks/Corpsparks.shtml
- Whitney Lake: Lofers Bend East (seasonal closure Oct 1–Mar 31 flagged), McCown Valley — https://www.swf-wc.usace.army.mil/whitney/Recreation/Parks/Corpsparks.shtml
Checked but not added: Waco, Somerville and Proctor Corps parks pages had no dump-station mention in park sections. Inventory is now 82 properties. Street addresses remain unset for lake-area listings.

## 2026-11-12 additions (local, unpublished)

Added 11 U.S. Army Corps of Engineers (Fort Worth District) properties from official park pages captured by direct HTTPS request on 2026-11-12 (`research/usace-{navarro,bardwell,lewisville,wrightpatman}.txt`; builder `scripts/add_2026_11_12.py`): Navarro Mills Lake (Liberty Hill, Wolf Creek, Oak Park, Pecan Point), Bardwell Lake (High View, Mott), Lewisville Lake (Hickory Creek, street address 1201 Point Vista Rd., Hickory Creek 75065), Wright Patman Lake (Clear Springs, Piney Point, Rocky Point, Malden Lake). Documented answers come only from those pages: Navarro Mills $4.00 dump fee for non-campers (fee + non-guest access), and park/campground seasons where stated. Gate hours are labeled as gate hours, not dump-station hours. Skipped: Bardwell Waxahachie Creek (page says CURRENTLY CLOSED), Wright Patman Oak Park (day-use only); lakes whose pages did not mention a dump station (Waco, Somerville, Proctor, Hords Creek, Aquilla, Benbrook, Grapevine, Lavon, Joe Pool, San Angelo, Pinkston, Sam Rayburn, Ferrells Bridge) were not added. Granger mentions a dump station only in a multi-park heading and was not added.

## 2026-11-13 additions (local, unpublished)

Added 7 federal campgrounds whose Recreation.gov facility record (the federal reservation system's own data, public endpoint `api/camps/campgrounds/<id>`, captured 2026-11-13 as `research/recgov-<id>.json` with sha256; builder `scripts/add_2026_11_13.py`) lists a dump station:
- USDA Forest Service: Ratcliff Lake Recreation Area (Davy Crockett NF, 18551 State Highway 7 East, Kennard 75487); Double Lake Recreation Area (Sam Houston NF, 301 FM 2025, Coldspring 77331; dump station use $5 per use).
- USACE Tulsa District: Pat Mayse West and Sanders Cove (Pat Mayse Lake area; year-round campgrounds); Juniper Point (Lake Texoma area; fully open Mar 1–Nov 30, Juniper East closed Dec 1–Feb 28) and Preston Bend (129 Preston Bend Park Road, Pottsboro 75076).
- National Park Service: Rio Grande Village Campground (Big Bend NP; dump/fill station at the campground entrance).
PO-box / project-office addresses were not used as campground addresses (Pat Mayse, Juniper Point, Rio Grande Village are named-area listings). Gate hours are labeled as gate hours. Inventory is now 100 properties.
Recreation.gov also lists a dump station for ~60 other Texas federal campgrounds (e.g. Lake O' the Pines, Sam Rayburn, Waco, Benbrook, Proctor, Somerville, Lavon, Steinhagen, Granger, Hords Creek parks, Chisos Basin and Cottonwood in Big Bend, Guadalupe Mountains Pine Springs) — candidate list in this pass; several of those lakes' USACE district pages did not mention a dump station, so Recreation.gov would be the sole source. Not yet added.

- 2026-11-14: +7 USACE Texas campgrounds with a Recreation.gov-listed dump station (Somerville Rocky Creek, Benbrook Holiday, Proctor Copperas Creek, Lake O' the Pines Brushy Creek, Steinhagen Magnolia Ridge, Sam Rayburn Rayburn Park, Lavon East Fork); named-area locations (Recreation.gov addresses are project offices); snapshots research/recgov-<id>.json. Total 107.
- 2026-11-15: +10 Texas federal campgrounds with a dump station in their Recreation.gov facility record (captured 2026-11-15, research/recgov-<id>.json + sha256; builder scripts/add_2026_11_15.py): USACE Alley Creek and Buckhorn Creek (Lake O' the Pines), Mill Creek, San Augustine and Twin Dikes (Sam Rayburn), Sandy Creek (Steinhagen; campground open year-round), Reynolds Creek (Waco Lake; campground sites open Apr 1–Sep 30), Plowman Creek and Kimball Bend (Whitney; year-round campgrounds); NPS Chisos Basin (Big Bend; 24 ft motor home / 20 ft trailer limit, oddly placed dump needs extra-long hose). Skipped: records with a "closed" notice (Hanks Creek, Ebenezer, Flatrock, Bear Creek, Mustang), records whose text says there is no dump station (Cottonwood, Pine Springs), and records without a dump amenity or sentence. Total 117. Published to main with the Nov 11–14 local additions.
- 2026-11-20: +6 Texas travel centers whose official location pages list an RV dump amenity (captured 2026-11-20, research/<id>-2026-11-20.txt + sha256; builder scripts/add_2026_11_20.py): Love's #200 Amarillo, #231 Hillsboro, #233 Waller, #242 San Antonio, #281 Fort Worth ("RV Dump Service" in each store's Amenities list) and TA Terrell #0233 ("RV Dump" in Other Amenities). Addresses from each page's PostalAddress. All question fields stay unknown (store hours/payment not assumed to apply to dumping). Recreation.gov re-scan found no new Texas campground with a dump amenity (Cottonwood, Pine Springs and Frijole Horse Corral state there is none; Rio Grande Village Group duplicates an existing property). Total 144.
