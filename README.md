# PageRank: A page ranking AI agent

Harvard CS50AI Project

## Description:

An AI program to rank web pages by importance inspired by Google PageRank's algorithms using both a Random Surfer Model and an Iterative Algorithm.

## Tech Stack:

* Python

## Background:

When search engines like Google display search results, they do so by placing more “important” and higher-quality pages higher in the search results than less important pages. But how does the search engine know which pages are more important than other pages?

One heuristic might be that an “important” page is one that many other pages link to, since it’s reasonable to imagine that more sites will link to a higher-quality webpage than a lower-quality webpage. We could therefore imagine a system where each page is given a rank according to the number of incoming links it has from other pages, and higher ranks would signal higher importance.

But this definition isn’t perfect: if someone wants to make their page seem more important, then under this system, they could simply create many other pages that link to their desired page to artificially inflate its rank.

For that reason, the PageRank algorithm was created by Google’s co-founders (including Larry Page, for whom the algorithm was named). In PageRank’s algorithm, a website is more important if it is linked to by other important websites, and links from less important websites have their links weighted less. This definition seems a bit circular, but it turns out that there are multiple strategies for calculating these rankings.

### Random Surfer Model

One way to think about PageRank is with the random surfer model, which considers the behavior of a hypothetical surfer on the internet who clicks on links at random. Consider the corpus of web pages below, where an arrow between two pages indicates a link from one page to another.

### Iterative Algorithm

We can also define a page’s PageRank using a recursive mathematical expression. Let PR(p) be the PageRank of a given page p: the probability that a random surfer ends up on that page. How do we define PR(p)? Well, we know there are two ways that a random surfer could end up on the page:

1. With probability 1 - d, the surfer chose a page at random and ended up on page p.
2. With probability d, the surfer followed a link from a page i to page p.

## Project Specification:

### transition_model
The transition_model should return a dictionary representing the probability distribution over which page a random surfer would visit next, given a corpus of pages, a current page, and a damping factor.

### sample_pagerank
The sample_pagerank function should accept a corpus of web pages, a damping factor, and a number of samples, and return an estimated PageRank for each page.

### iterate_pagerank
The iterate_pagerank function should accept a corpus of web pages and a damping factor, calculate PageRanks based on the iteration formula described above, and return each page’s PageRank accurate to within 0.001.

## How to run

1. Clone this project
2. Run the PageRank AI:
   ```
   python pagerank.py 'dataset file'
   ```
   (You can use either `corpus0` or `corpus1` or `corpus2` for the dataset file)
