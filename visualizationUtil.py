class visualizationUtil:
	#this file can be opened by GVEdit or Gephi
	def generateDotFile(self, data, file_name):
		if not data:
			print 'not data to generate!'
			return

		OUT = file_name+".dot"
		dot = ['"%s" -> "%s" [weibo_id=%s]' % (data[weibo_id][1].encode('utf-8','ignore'), data[weibo_id][0].encode('utf-8','ignore'), weibo_id) for weibo_id in data.keys()]
		with open(OUT,'w') as f:
			f.write('strict digraph {\nnode [fontname="FangSong"]\n%s\n}' % (';\n'.join(dot),))
			print 'dot file export'	

	#GDF is more powerful than dot, can be opened by Gephi
	#see format at http://gephi.org/users/supported-graph-formats/gdf-format/ 
	def generateGDFfile(self, data, file_name):
		if not self.repost:
			print 'not data to generate!'
			return	

		OUT = file_name+ '.gdf'
		with open(OUT,'w') as f:
			f.write('nodedef>name VARCHAR,label VARCHAR\n')
			#add notedata
			f.write('edgedef>node1 VARCHAR,node2 VARCHAR\n')
			#add edgedata
			print 'dot file export'	

	#just generate TagCloud File,and open with webbrowser,
	#because generate tagcloud image file directly is too complicate :(
	def generateTagCloudFile(self, content, minfontsize=3, maxfontsize=20, topk=10):
		if not content:
			print 'empty data!!!'
			return
		HTML_TEMPLATE = './html/tagcloud_template.html'
		top_tuples = self.getKeyword(content, topk)
		print top_tuples
		min_freq, max_freq = top_tuples[topk-1][0], top_tuples[0][0]
		weighted_output = [(v, '', (k - min_freq) * (maxfontsize - minfontsize)/(max_freq - min_freq) + minfontsize) for k,v in top_tuples]
		htmlPage = open(HTML_TEMPLATE).read() % \
		    (json.dumps(weighted_output),)

		if not os.path.isdir('out'):
			os.mkdir('out')

		f = open(os.path.join('out', os.path.basename(HTML_TEMPLATE)), 'w')
		f.write(htmlPage)
		f.close()

		print 'Tagcloud stored in: %s' % f.name

		# Open up the web page in your browser
		webbrowser.open("file://" + os.path.join(os.getcwd(), 'out', os.path.basename(HTML_TEMPLATE)))

	# Writes out an HTML page that can be opened in the browser
	# that displays a graph 	
	# it doen't work :( will fix some times 
	def generateProtovis(self):
		if not self.repost:
			print 'not data to generate!'
			return
		HTML_TEMPLATE = './html/repost_graph.html'
		g = nx.DiGraph()
		for weibo_id in self.repost.keys():
			g.add_edge(self.repost[weibo_id][1].encode('utf-8','ignore'), self.repost[weibo_id][0].encode('utf-8','ignore'), weibo_id)

		nodes = g.nodes()
		indexed_nodes = {}

		idx = 0
		for n in nodes:
			indexed_nodes.update([(n, idx,)])
			idx += 1

		links = []
		for n1, n2 in g.edges():
			links.append({'source' : indexed_nodes[n2], 
			              'target' : indexed_nodes[n1]})

		json_data = json.dumps({"nodes" : [{"nodeName" : n} for n in nodes], "links" : links}, indent=4)
		html = open(HTML_TEMPLATE).read() % (json_data,)
		if not os.path.isdir('out'):
			os.mkdir('out')
		f = open(os.path.join(os.getcwd(), 'out', os.path.basename(HTML_TEMPLATE)), 'w')
		f.write(html)
		f.close()

		print >> sys.stderr, 'Data file written to: %s' % f.name


		webbrowser.open('file://' + f.name)