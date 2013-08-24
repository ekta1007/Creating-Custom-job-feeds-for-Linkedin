Creating-Custom-job-feeds-for-Linkedin
======================================

This project has two parts 
Part 1 : Creating a quick csv file from the job pages from Linkedin using url_open & clean html contructs (for quick-win) and having some predefined filters, for location, and other advanced filters. 
In general all the 'jobs" at linkedin follow one of the below categories -:
1. The job you're looking for is no longer active
2  We can't find the job you're looking for
3  The job passes your filtering criteria (location, Skill-specific keywords etc)
4  The job is active, but does not pass your ltering criteria

Looping constructs extend this list and can virtually go (snoop) around a lot more pages
I exploit this to find and narrow down our corpus so that the tokenization in part 2, which is based on urls of interest from part 1 , is smart and quick

Part 2 : I use the TF-IDF on the base (resume of interest) and other jobs (urls shortlisted from Part 1, or otherwise), and develop similarity between the Job posting and the base resume.

Finally I will do the visualizable in Gephi. 
