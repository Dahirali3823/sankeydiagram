# Sankey Diagram

## The goal of this project is to produce a Sankey diagram of my job search using job application emails and categorizing them

The first thing i did was to brainstorm on the system design process and how i was going to approach this project

I had a couple options:

1) Use the gmail api to fetch emails and search for key words to filter for job application related emails
2) Download all my emails and write a script searching through those emails using filters and keywords
3) Use the gmail website itself and search for emails through there


I decided to use an option that combines a little bit of three:

I manually tagged emails and categorized into labels them using the search on the gmail website and writing multiple filters to find them

I tagged them into these categories:

Applications, Interview, 1st round, 2nd round, 3rd Round, Offer, Accepted, Rejected

Once i got my labels and emails categorized to the best of my ability i started to read the GMAIL API documentation

I used some starter code already provided to authenticate my account and set up any credentials needed such as OAuth Token

I then wrote a function to retrieve the application labels on my gmail account once i verified it

Initially i tried to use the plotly library to draw a sankey diagram however it was tedious and it didn't look as good as i expected it to be 

I really am a fan of the Sankeymatic.com website as it was my insipration for this project so i tried to find a way to use it/implement it to get beautiful diagrams

Sankeymatic doesn't have any API so the next best option i had was to use Selenium to automate a browser to the SankeyMatic website, go to the job search diagram and enter a formatted text input to diagram and download and save it to my computer


Problems/issues as of 02/08/25:
1. Need to be able to authenticate multiple accounts in one go
2. Need to be able to retrive labels of all accounts in one go
3. Need to collect and format label info into appropiate format with all labels correctly accounted for
4. Need to use selenium to input the formatted text 
5. Download Job Diagram to folder



I was able to authenticate multiple accounts by rewriting my authentication function to take in an email and account number and creating credentials and verifying them. I also was able to rewrite my label functions to accurately correct labels such as ensuring conversations in one email don't get counted, ensuring a chain of emails from the same email regarding different job applications are handled correctly and also combining the labels of my two emails into one.


From there i rewrote my format function to return an array of formatted strings that have the correct information with a escaped line after everyone(similiar to how sankeymatic accepts input)

I then needed to reconfigure selenium file and after some research and reading documentation i learnt about webdrivers and how i can use the html and inspect/dev tools on chrome to manipulate the website and enter my formatted text in. I then downloaded the png and closed the tab.