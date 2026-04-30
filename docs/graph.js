let cy = null;

function initGraph() {
  if (cy) {
    return;
  }

  fetch('./manifest.json')
    .then(function (response) {
      return response.json();
    })
    .then(function (manifest) {
      var imageMap = {};
      (manifest.artifacts || []).forEach(function (artifact) {
        imageMap[artifact.id] = artifact.image_url || '';
      });
      return imageMap;
    })
    .catch(function () {
      return {};
    })
    .then(function (imageMap) {
      return fetch('data/graph.json')
        .then(function (response) {
          return response.json();
        })
        .then(function (graphData) {
          return { graphData: graphData, imageMap: imageMap };
        });
    })
    .then(function (result) {
      var graphData = result.graphData;
      var imageMap = result.imageMap;

      // Enrich node data with image_url
      if (graphData.elements && graphData.elements.nodes) {
        graphData.elements.nodes.forEach(function (node) {
          node.data.image_url = imageMap[node.data.id] || '';
        });
      }

      cy = cytoscape({
        container: document.getElementById('cy'),
        elements: graphData.elements,
        style: [
          {
            selector: 'node',
            style: {
              label: 'data(label_en)',
              'background-color': '#4a7c59',
              color: '#fff',
              'text-valign': 'center',
              'text-halign': 'center',
              'font-size': '10px',
              width: '50px',
              height: '50px',
            },
          },
          {
            selector: 'node[image_url != ""]',
            style: {
              'background-image': 'data(image_url)',
              'background-fit': 'cover',
              'background-clip': 'node',
              'text-opacity': 1,
              'text-background-color': 'rgba(10, 10, 10, 0.72)',
              'text-background-opacity': 1,
              'text-background-padding': '3px',
              'text-margin-y': '36px',
            },
          },
          {
            selector: 'edge',
            style: {
              width: 1,
              opacity: 0.8,
            },
          },
          {
            selector: 'edge[type = "era"]',
            style: {
              'line-color': '#6699cc',
            },
          },
          {
            selector: 'edge[type = "category"]',
            style: {
              'line-color': '#66aa77',
            },
          },
          {
            selector: 'edge[type = "location"]',
            style: {
              'line-color': '#cc9944',
            },
          },
          {
            selector: 'edge[type = "material"]',
            style: {
              'line-color': '#9966cc',
            },
          },
        ],
        layout: {
          name: 'cose',
          nodeRepulsion: function () {
            return 450000;
          },
          idealEdgeLength: function () {
            return 150;
          },
          nodeOverlap: 20,
          gravity: 80,
          componentSpacing: 100,
          padding: 30,
          fit: true,
        },
      });

      cy.on('tap', 'node', function (evt) {
        showDetail(evt.target.data('id'));
      });

      cy.on('mouseover', 'node', function (evt) {
        evt.target.style({ width: '80px', height: '80px' });
      });

      cy.on('mouseout', 'node', function (evt) {
        evt.target.style({ width: '50px', height: '50px' });
      });

      if (typeof currentLang !== 'undefined') {
        updateGraphLabels(currentLang);
      }

      filterEdges(['era', 'category', 'location', 'material']);
    })
    .catch(function (error) {
      console.error('Failed to initialize graph:', error);
    });
}

function filterEdges(activeTypes) {
  if (!cy) return;

  cy.edges().forEach(function (e) {
    if (activeTypes.indexOf(e.data('type')) !== -1) {
      e.show();
    } else {
      e.hide();
    }
  });
}

function updateGraphLabels(lang) {
  if (!cy) return;

  var labelField = lang === 'en' ? 'label_en' : 'label_ko';
  cy.nodes().style('label', function (ele) {
    return ele.data(labelField);
  });
}

function getGraphInstance() {
  return cy;
}
