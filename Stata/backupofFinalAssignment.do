// The assignment

cd D:\Lab\Stata

// br respondent_age age_1 age_2 age_3 age_4 age_5 random_mem_id agegroup



use "SCS_data.dta"

// 1. Create age group for respondents (agegroup):
generate respondent_age = .


forvalues i = 1/17 {
    replace respondent_age = age_`i' if random_mem_id == "`i'"
}


gen agegroup = .

replace agegroup = 1 if respondent_age < 5
replace agegroup = 2 if inrange(respondent_age, 6, 12)
replace agegroup = 3 if inrange(respondent_age, 13, 18)
replace agegroup = 4 if inrange(respondent_age, 19, 30)
replace agegroup = 5 if inrange(respondent_age, 31, 45)
replace agegroup = 6 if inrange(respondent_age, 46, 60)
replace agegroup = 7 if respondent_age > 60


// 2. Create total contact variable (allnoncontact)


//br meet_people_1 meet_people_2 meet_people_3 meet_people_4 place_house_1 place_house_2 place_house_3 place_house_4
// br meet_people_1 meet_people_2 meet_people_3
// br enumid meet_people_1 meet_people_2 meet_people_3 allnoncontact
// br allnoncontact

// drop allnoncontact

egen allnoncontact = rowtotal(meet_people_*) 

//foreach var of varlist meet_people_* {
//    replace allnoncontact = allnoncontact + `var'
//}

// to check if you are correct 
//list meet_people_* allnoncontact if allnoncontact > 0


// 3. Create a variable identifying the day of the survey date (day)


//drop prev_day
//drop day_of_week

generate prev_day = startdate - 1
generate day_of_week = dow(prev_day) //dow returens the day of the week like 0 Sunday , 1 Monday

generate day = ""
replace day = "Friday" if day_of_week == 5
replace day = "Saturday" if day_of_week == 6
replace day = "Weekday" if day_of_week >= 0 & day_of_week <= 4


// 4. Create sex variable (sex)

//substr(string, start, length)

generate strata_code = real(substr(village_strata, strpos(village_strata, "-") + 1, .))

generate sex = ""
replace sex = "Female" if inlist(strata_code, 1, 3, 5)
replace sex = "Male" if inlist(strata_code, 2, 4, 6)

//br enumid  village_strata  sex

//5. 
twoway (histogram allnoncontact if sex == "Male", by(agegroup) percent  fcolor(blue%50) lwidth(none) lcolor(none)) ///
       (histogram allnoncontact if sex == "Female", by(agegroup) percent  fcolor(red%50) lwidth(none) lcolor(none)), ///
       legend(order(1 "Male" 2 "Female") ///
              position(4) title("Sex") size(medium) nobox col(1)) ///
       graphregion(color(white) lwidth(none) lcolor(white))

histogram allnoncontact , discrete fraction by(agegroup) gap(40) xlabel(2 3 4, valuelabel)

//////////////

* Filter for age group 1 (<5 years)
gen agegroup1 = agegroup == 1

* Create separate variables for male and female in age group 1
gen allnoncontact_male = allnoncontact if sex == "Male" & agegroup1
gen allnoncontact_female = allnoncontact if sex == "Female" & agegroup1

* Plot histogram for Male (blue) and Female (red) and normalize to percentages
twoway ///
(histogram allnoncontact_male, color(blue%50) percent width(5)) ///
(histogram allnoncontact_female, color(red%50) percent width(5)), ///
legend(order(1 "Male" 2 "Female")) ///
ytitle("Percentage") ///
xtitle("Number of Non-Household Contacts") ///
title("<5 years Age Group: Non-Household Contacts by Sex") ///
saving(F1_hhcontacts, replace)

////////////////

* Create a new variable for each age group
drop allnoncontact_male
drop allnoncontact_female
gen allnoncontact_male = allnoncontact if sex == "Male"
gen allnoncontact_female = allnoncontact if sex == "Female"

//test

twoway (histogram allnoncontact_male if agegroup == 1, color(blue%50) percent width(5)) ///
          (histogram allnoncontact_female if agegroup == 1, color(red%50) percent width(5)), ///
          title("<5 years (N=194)")
twoway (histogram allnoncontact_male if agegroup == 2, color(blue%50) percent width(5)) ///
          (histogram allnoncontact_female if agegroup == 2, color(red%50) percent width(5)), ///
          title("6-12 years (N=657)")

//test


* Create a combined graph with panels for each age group
graph combine ///
    (twoway (histogram allnoncontact_male if agegroup == 1, color(blue%50) percent width(5)) ///
            (histogram allnoncontact_female if agegroup == 1, color(red%50) percent width(5)), ///
            title("<5 years (N=194)")) ///
    (twoway (histogram allnoncontact_male if agegroup == 2, color(blue%50) percent width(5)) ///
            (histogram allnoncontact_female if agegroup == 2, color(red%50) percent width(5)), ///
            title("6-12 years (N=657)")) ///
    (twoway (histogram allnoncontact_male if agegroup == 3, color(blue%50) percent width(5)) ///
            (histogram allnoncontact_female if agegroup == 3, color(red%50) percent width(5)), ///
            title("13-18 years (N=532)")) ///
    (twoway (histogram allnoncontact_male if agegroup == 4, color(blue%50) percent width(5)) ///
            (histogram allnoncontact_female if agegroup == 4, color(red%50) percent width(5)), ///
            title("19-30 years (N=436)")) ///
    (twoway (histogram allnoncontact_male if agegroup == 5, color(blue%50) percent width(5)) ///
            (histogram allnoncontact_female if agegroup == 5, color(red%50) percent width(5)), ///
            title("31-45 years (N=664)")) ///
    (twoway (histogram allnoncontact_male if agegroup == 6, color(blue%50) percent width(5)) ///
            (histogram allnoncontact_female if agegroup == 6, color(red%50) percent width(5)), ///
            title("45-60 years (N=332)")) ///
    (twoway (histogram allnoncontact_male if agegroup == 7, color(blue%50) percent width(5)) ///
            (histogram allnoncontact_female if agegroup == 7, color(red%50) percent width(5)), ///
            title("60+ years (N=172)")), ///
    legend(order(1 "Male" 2 "Female") position(6)) ///
    ytitle("Percentage") ///
    xtitle("Number of Non-Household Contacts") ///
    saving(F1_combined_hhcontacts, replace)


* Export the graph as PNG
graph export "F1_combined_hhcontacts.png", replace


/////////// trial 3 

twoway (histogram allnoncontact_male if agegroup == 1, color(blue%50) percent width(5)) ///
       (histogram allnoncontact_female if agegroup == 1, color(red%50) percent width(5)), ///
       title("<5 years (N=194)") saving(graph1, replace)

twoway (histogram allnoncontact_male if agegroup == 2, color(blue%50) percent width(5)) ///
       (histogram allnoncontact_female if agegroup == 2, color(red%50) percent width(5)), ///
       title("6-12 years (N=657)") saving(graph2, replace)

twoway (histogram allnoncontact_male if agegroup == 3, color(blue%50) percent width(5)) ///
       (histogram allnoncontact_female if agegroup == 3, color(red%50) percent width(5)), ///
       title("13-18 years (N=532)") saving(graph3, replace)

twoway (histogram allnoncontact_male if agegroup == 4, color(blue%50) percent width(5)) ///
       (histogram allnoncontact_female if agegroup == 4, color(red%50) percent width(5)), ///
       title("19-30 years (N=436)") saving(graph4, replace)

twoway (histogram allnoncontact_male if agegroup == 5, color(blue%50) percent width(5)) ///
       (histogram allnoncontact_female if agegroup == 5, color(red%50) percent width(5)), ///
       title("31-45 years (N=664)") saving(graph5, replace)

twoway (histogram allnoncontact_male if agegroup == 6, color(blue%50) percent width(5)) ///
       (histogram allnoncontact_female if agegroup == 6, color(red%50) percent width(5)), ///
       title("45-60 years (N=332)") saving(graph6, replace)

twoway (histogram allnoncontact_male if agegroup == 7, color(blue%50) percent width(5)) ///
       (histogram allnoncontact_female if agegroup == 7, color(red%50) percent width(5)), ///
       title("60+ years (N=172)") saving(graph7, replace)
	   
graph combine graph1.gph graph2.gph graph3.gph graph4.gph graph5.gph graph6.gph graph7.gph  ///
              legend(order(1 "Male" 2 "Female") position(6)) ///
              ytitle("Percentage") ///
              xtitle("Number of Non-Household Contacts") ///
              saving(F1_combined_hhcontacts, replace)

graph combine graph1.gph graph2.gph graph3.gph graph4.gph graph5.gph graph6.gph graph7.gph,col(3)
      imargin(0 0 0 0) graphregion(margin(l=22 r=22))
	  title("Life expectancy at birth vs. GNP per capita")
	  note("Source: 1998 data from The World Bank Group")


// 6 
gen agegroup1 = agegroup == 1  // Create a variable to filter for agegroup 1

collapse (count) allnoncontact, by(agegroup1 sex)  // Summarize the data by age group and sex

graph bar (percent) allnoncontact, over(agegroup1, gap(0)) over(sex, gap(0)) ///
    bar(1, color(red)) bar(2, color(blue)) ///
    ytitle("Percentage") title("Non-Household Contacts by Age Group 1 and Sex") ///
    name(F1_hhcontacts, replace)

