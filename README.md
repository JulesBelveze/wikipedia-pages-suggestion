 <h1>Final project description </h1>

  The idea of our group is to work on related Wikipedia pages. That is to give as input a Wikipedia page and to get related pages’ name as output. 
The idea is to go through the first page text and to get all Wikipedia pages mentioned. 
Then go through all that pages and get all Wikipedia pages mentioned and so on until we have visited a specific number of pages. 
By doing it some pages will been mentioned many times and so they should be related to input page. 
It can be seen as a network where nodes are Wikipedia pages and there is a path from node A to node B if page B is mentioned in page A. 
Thus the intention is to retrieve the most linked nodes which there is a path from the input one.

  Here is a short description of the steps will have to go through :
<li>Be able to extract Wikipedia links from a page. &#9989;</li>
<li>Define a relevant criteria to stop going through pages.</li>
<li>Construct a network where nodes are pages and draw an edge from A to B if B is mentionned in page A. </li>
<li>Construct a PageRank. May use MapReduce for the matrix product in PageRank.</li>
<li>Cluster all pages (which similarity ?).</li>
<li>Display the nodes with the highest page rank of each cluster.</li>

<br>Bonus idea : network statistics
