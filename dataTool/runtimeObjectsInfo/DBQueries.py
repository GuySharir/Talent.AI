JOB_OFFER_QUERY = """query Query($getJobOfferInput: GetJobOfferInput!) {
                      getJobOffer(getJobOfferInput: $getJobOfferInput) {
                        full_name
                        first_name
                        last_name
                        gender
                        birth_year
                        birth_date
                        industry
                        job_title
                        job_title_role
                        job_title_sub_role
                        job_title_levels
                        job_company_id
                        job_company_name
                        job_start_date
                        interests
                        skills
                        experience {
                          company_name
                          company_founded
                          company_industry
                          company_size
                          current_job
                          company_location_name
                          company_location_country
                          company_location_continent
                          end_date
                          start_date
                          title_name
                          title_role
                          title_levels
                        }
                        education {
                          school_name
                          school_type
                          degrees
                          start_date
                          end_date
                          majors
                          minors
                          gpa
                        }
                      }
                    }"""

CANDIDATE_QUERY = """query GetCandidatesByFullName($getCandidatesInputFullName: GetCandidatesInputFullName!) {
                        getCandidatesByFullName(getCandidatesInputFullName: $getCandidatesInputFullName) {
                            full_name
                            first_name
                            last_name
                            gender
                            birth_date
                            industry
                            job_title
                            job_title_role
                            job_title_sub_role
                            job_title_levels
                            job_company_id
                            job_company_name
                            job_start_date
                            interests
                            skills
                            experience {
                              company_name
                              company_industry
                              company_size
                              current_job
                              company_location_name
                              company_location_country
                              company_location_continent
                              end_date
                              start_date
                              title_name
                              title_role
                              title_levels
                            }
                            education {
                              school_name
                              school_type
                              degrees
                              start_date
                              end_date
                              majors
                              minors
                            }
                        }
                }"""
