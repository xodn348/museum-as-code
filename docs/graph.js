let cy = null;

function initGraph() {
  if (cy) {
    return;
  }

  fetch('data/graph.json')
    .then(function (response) {
      return response.json();
    })
    .then(function (graphData) {
      cy = cytoscape({
        container: document.getElementById('cy'),
        elements: graphData.elements,
        style: [
          {
            selector: 'node',
            style: {
              label: 'data(label_ko)',
              'background-color': '#4a7c59',
              color: '#fff',
              'text-valign': 'center',
              'text-halign': 'center',
              'font-size': '10px',
              width: '30px',
              height: '30px',
              cursor: 'pointer',
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
          nodeRepulsion: function (node) {
            return 6000;
          },
          animate: false,
          randomize: true,
        },
      });

      cy.on('tap', 'node', function (evt) {
        showDetail(evt.target.data('id'));
      });

      if (typeof currentLang !== 'undefined') {
        updateGraphLabels(currentLang);
      }

      filterEdges(['category']);
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
