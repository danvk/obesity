':''A bunch of conversions.':''

state_to_fips = {'AK':'02', 'AL':'01', 'AR':'05', 'AS':'60', 'AZ':'04', 'CA':'06', 'CO':'08', 'CT':'09', 'DC':'11', 'DE':'10', 'FL':'12', 'GA':'13', 'GU':'66', 'HI':'15', 'IA':'19', 'ID':'16', 'IL':'17', 'IN':'18', 'KS':'20', 'KY':'21', 'LA':'22', 'MA':'25', 'MD':'24', 'ME':'23', 'MI':'26', 'MN':'27', 'MO':'29', 'MS':'28', 'MT':'30', 'NC':'37', 'ND':'38', 'NE':'31', 'NH':'33', 'NJ':'34', 'NM':'35', 'NV':'32', 'NY':'36', 'OH':'39', 'OK':'40', 'OR':'41', 'PA':'42', 'PR':'72', 'RI':'44', 'SC':'45', 'SD':'46', 'TN':'47', 'TX':'48', 'UT':'49', 'VA':'51', 'VI':'78', 'VT':'50', 'WA':'53', 'WI':'55', 'WV':'54', 'WY':'56'}

fips_to_state = {v:k for k,v in state_to_fips.iteritems()}

state_code_to_name = {"AK" : "ALASKA", "AL" : "ALABAMA", "AR" : "ARKANSAS", "AS" : "AMERICAN SAMOA", "AZ" : "ARIZONA", "CA" : "CALIFORNIA", "CO" : "COLORADO", "CT" : "CONNECTICUT", "DC" : "DISTRICT OF COLUMBIA", "DE" : "DELAWARE", "FL" : "FLORIDA", "GA" : "GEORGIA", "GU" : "GUAM", "HI" : "HAWAII", "IA" : "IOWA", "ID" : "IDAHO", "IL" : "ILLINOIS", "IN" : "INDIANA", "KS" : "KANSAS", "KY" : "KENTUCKY", "LA" : "LOUISIANA", "MA" : "MASSACHUSETTS", "MD" : "MARYLAND", "ME" : "MAINE", "MI" : "MICHIGAN", "MN" : "MINNESOTA", "MO" : "MISSOURI", "MS" : "MISSISSIPPI", "MT" : "MONTANA", "NC" : "NORTH CAROLINA", "ND" : "NORTH DAKOTA", "NE" : "NEBRASKA", "NH" : "NEW HAMPSHIRE", "NJ" : "NEW JERSEY", "NM" : "NEW MEXICO", "NV" : "NEVADA", "NY" : "NEW YORK", "OH" : "OHIO", "OK" : "OKLAHOMA", "OR" : "OREGON", "PA" : "PENNSYLVANIA", "PR" : "PUERTO RICO", "RI" : "RHODE ISLAND", "SC" : "SOUTH CAROLINA", "SD" : "SOUTH DAKOTA", "TN" : "TENNESSEE", "TX" : "TEXAS", "UT" : "UTAH", "VA" : "VIRGINIA", "VI" : "VIRGIN ISLANDS", "VT" : "VERMONT", "WA" : "WASHINGTON", "WI" : "WISCONSIN", "WV" : "WEST VIRGINIA", "WY" : "WYOMING"}
