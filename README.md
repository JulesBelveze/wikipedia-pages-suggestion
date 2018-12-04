 <h1>Final project description </h1>

  The idea of our group is to work on related Wikipedia pages. That is to give as input a Wikipedia page and to get related pages’ name as output. 
The idea is to go through the first page text and to get all Wikipedia pages mentioned. 
Then go through all that pages and get all Wikipedia pages mentioned and so on until we have visited a specific number of pages. 
By doing it some pages will been mentioned many times and so they should be related to input page. 
It can be seen as a network where nodes are Wikipedia pages and there is a path from node A to node B if page B is mentioned in page A. 
Thus the intention is to retrieve the most linked nodes which there is a path from the input one.

  Here is a short description of the steps will have to go through :
<li>Be able to extract Wikipedia links from a page. &#9989;</li>
<li>Define a relevant criteria to stop going through pages (experimentaly). Option : compute the number of occurences of pages. &#9989;</li>
<li>Construct a network where nodes are pages and draw an edge from A to B if B is mentionned in page A. &#9989; </li>
<li>Construct a PageRank &#9989;.</li>
<li>Cluster all pages using either K-Mean or DBSCAN &#9989;.</li>
<li>Display the nodes with the highest page rank of each cluster &#9989;.</li>

<hr>

<h1> User's guide :</h1>
First you have to be sure that all packages are already installed. </br>
To install the ForceAtlas2 : <code> pip install fa2 </code> </br>
To install Networkx : <code> pip install networkx </code> </br>

<p> Now you are ready to use our program.<br>
 
<li>The first step is to create the graph of your desire input and then to save it as a .gml file. To do so run the <var>graphConstructor.py</var> file and fill out the inputs with your desired parameters. <br>
The first parameter is the title of the <i>Wikipedia</i> page you want suggestions about. The second one is the depth limit (we recommend you not to exceed 3 otherwise it will take a really long time to run and the suggested pages might off subject from the input.</li> <br>
 
 <li>Then run the <var>graphAnalyzer.py</var> file. This will display a list of all the suggested pages and their related PageRank. It will also create a graph called <var>graph_with_layout.png</var> where you will be able to identify the different clusters.</li> <br>
 
 <b>Warning :</b> Please keep in mind that the DBSCAN algorithm does not provide a really relevant output and that it might take up to 10min to run. Therefore, we recommend you to use the K-Means algorithm (that is to give False as input when running <var>graphAnalyzer.py</var>)
