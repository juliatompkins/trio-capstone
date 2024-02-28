library(tidycensus)
library(tidyverse)
setwd("/Users/dylanmack/Library/CloudStorage/OneDrive-WashingtonUniversityinSt.Louis/ESE 499/trio-capstone")
census_api_key("67c9126453c8bf858be1685cb7e4c9a48c712f5c", install = TRUE)

acs_20_vars = load_variables(
  year = 2020, 
  "acs5",
  cache = TRUE
)

commute_by_income = get_acs(geography = "tract", state = "MO", county = "St. Louis city", table = "B08119", cache_table = TRUE) %>%
  rename(name = variable, location = NAME) %>%
  left_join(acs_20_vars, by = "name") 


block_level_transit_mode = get_acs(geography = "block group", state = "MO", county = "St. Louis city", table = "B08301") %>%
  rename(name = variable, location = NAME) %>%
  left_join(acs_20_vars, by = "name") 




B08119_stl_city = get_acs(geography = "tract", state = "MO", county = "St. Louis city", table = "B08119", cache_table = TRUE) %>%
  rename(name = variable, location = NAME) %>%
  left_join(acs_20_vars, by = "name")

B08119_stl_county = get_acs(geography = "tract", state = "MO", county = "St. Louis County", table = "B08119", cache_table = TRUE) %>%
  rename(name = variable, location = NAME) %>%
  left_join(acs_20_vars, by = "name")


block_level_transit_vars = acs_20_vars %>%
  filter(grepl("block group", geography, ignore.case = TRUE)) %>%
  filter(grepl("trans", concept, ignore.case = TRUE))






letters = c('B', 'C', 'D', 'E', 'F', 'G', 'H', 'I')

B08105_stl_city = get_acs(geography = "tract", state = "MO", county = "St. Louis city", table = "B08105A", cache_table = TRUE) %>%
  rename(name = variable, location = NAME) %>%
  left_join(acs_20_vars, by = "name")

for (letter in letters) {
  placeholder = get_acs(geography = "tract", state = "MO", county = "St. Louis city", table = paste("B08105", letter, sep = ""), cache_table = TRUE) %>%
    rename(name = variable, location = NAME) %>%
    left_join(acs_20_vars, by = "name")
  B08105_stl_city = rbind(B08105_stl_city, placeholder)
}



