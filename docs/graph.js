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
              label: 'data(label_en)',
              'background-color': '#1f2a21',
              'border-color': '#d9b45e',
              'border-width': '2px',
              color: '#f6efe3',
              'text-valign': 'center',
              'text-halign': 'center',
              'font-family': 'Georgia, serif',
              'font-size': '10px',
              'text-wrap': 'wrap',
              'text-max-width': '86px',
              'text-background-color': 'rgba(9, 13, 10, 0.84)',
              'text-background-opacity': 1,
              'text-background-padding': '4px',
              width: '72px',
              height: '72px',
            },
          },
          {
            selector: 'edge',
            style: {
              width: 1,
              opacity: 0.62,
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
        evt.target.style({ width: '96px', height: '96px' });
      });

      cy.on('mouseout', 'node', function (evt) {
        evt.target.style({ width: '72px', height: '72px' });
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
