import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    # Check if current page has no links to other pages
    if len(corpus[page]) == 0:

        # Return the dictionary with equally probability distribution to each page in dictionary
        return {p: (1 / len(corpus)) for p in corpus}

    # Create dictionary for all pages in the corpus
    d = {}

    # Calculate probability of choosing a link at random linked to by `page` with probability `damping_factor`
    rand_link_page = damping_factor / len(corpus[page])

    # Calculate probability of choosing a link at random chosen from all pages in the corpus with probability `1 - damping_factor`
    rand_page_corpus = (1 - damping_factor) / len(corpus)

    # Loop through each page in the corpus
    for p in corpus:

        # Assign probability of choosing a link at random chosen from all pages in the corpus with probability `1 - damping_factor`
        # If the page has a link in current page on then we add the probability of choosing a link at random linked to by `page` with probability `damping_factor`
        d[p] = rand_page_corpus + rand_link_page if p in corpus[page] else rand_page_corpus

    # Return the dictionary
    return d


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Create dictionary for all pages in corpus
    d = {p: 0 for p in corpus}

    # Get the first sample randomly
    cur_sample = random.choice(list(corpus.keys()))
    d[cur_sample] += 1

    # Generate all remaining sample
    for _ in range(n - 1):

        # Using transition model to generate next sample probability dictionary
        next_sample_dict = transition_model(corpus, cur_sample, damping_factor)

        # Get the list of pages from the dictionary of next sample
        next_sample_population = list(next_sample_dict.keys())

        # Get the list of probability for each page
        next_sample_weight = list(next_sample_dict.values())

        # Get the next sample page
        next_sample = random.choices(next_sample_population, weights=next_sample_weight, k=1)[0]

        # Counting number of times page shown up
        d[next_sample] += 1

        # Set the current sample to next sample page
        cur_sample = next_sample

    # Return dictionary with page’s estimated PageRank (the proportion of all the samples that corresponded to that page)
    return {p: (d[p] / n) for p in corpus}


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Create dictionary for all pages in corpus and assign each page a rank of 1/N where N is the total number of pages in corpus
    d = {p: (1 / len(corpus)) for p in corpus}

    # Create a dictionary to store new rank value after calculating with PageRank formula
    new_d = {p: 0 for p in corpus}

    # Set PageRank value change
    pr_value_change = 0.002

    # Repeatedly calculating until no PageRank value changes by more than 0.001
    while pr_value_change > 0.001:

        # Loop through each page in corpus
        for p1 in corpus:

            # Set up summation variable for second condition of formula required calulating iteratively
            summation = 0

            # Loop through every pages to consider any pages that links to current page
            for p2 in corpus:

                # Check if p2 links to p1
                if p1 in corpus[p2]:

                    # Add up to second condition variable
                    summation += (d[p2] / len(corpus[p2]))

                # If p2 has no links
                if len(corpus[p2]) == 0:

                    # Interpreted as having one link for every page in the corpus (including itself)
                    summation += (d[p2] / len(corpus))

            # Calculate new rank value and update it to dictionary
            new_d[p1] = ((1 - damping_factor) / len(corpus)) + (damping_factor * summation)

        # Loop through each page to compare and check the page rank value change
        for page in corpus:

            # Calculate rank value difference between new value and current value
            rank_value_change = abs(d[page] - new_d[page])

            # Set variable to that value
            pr_value_change = rank_value_change

            # If the difference still larger than 0.001 then break the for loop to keep the while loop repeatedly calculating again
            if pr_value_change > 0.001:
                break

        # Update the dictionary
        d = new_d.copy()

    # Return the dictionary
    return d


if __name__ == "__main__":
    main()
