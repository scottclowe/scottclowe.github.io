---
layout: default
title: Publications
---

<h1>Publications</h1>

<p>For a full publications list, please see my <a href="https://scholar.google.com/citations?user=ZFPhxuAAAAAJ">Google Scholar</a> page.</p>

<!-- Topic Filters -->
<div id="topic-filters">
  <p>Filter by topic:</p>
</div>
<button id="select-all">Select all topics</button>
<button id="select-none">Deselect all topics</button>

<!-- Container for Publications -->
<div id="publications-container">
  <!-- Publications will be dynamically inserted here -->
</div>

<!-- JavaScript for Interactivity -->
<script>
  // Publications data from YAML (inserted by Jekyll)
  const publications = {{ site.data.publications | jsonify }};

  // Populate the topic filters
  const topics = new Set(publications.flatMap(pub => pub.topics));
  const topicFilters = document.getElementById('topic-filters');

  topics.forEach(topic => {
    const topicElement = document.createElement('div');
    topicElement.className = 'topic-filter selected';
    topicElement.textContent = topic;
    topicElement.dataset.topic = topic;

    topicElement.addEventListener('click', () => {
      topicElement.classList.toggle('selected');
      renderPublications();
    });

    topicFilters.appendChild(topicElement);
  });

  // Function to render publications
  function renderPublications() {
    selectedTopics = Array.from(document.querySelectorAll('.topic-filter.selected'))
      .map(el => el.dataset.topic);

    if (selectedTopics.length == 0) {
        selectedTopics = Array.from(document.querySelectorAll('.topic-filter'))
            .map(el => el.dataset.topic);
    }

    const container = document.getElementById('publications-container');
    container.innerHTML = ''; // Clear current content

    const filteredPublications = publications.filter(pub =>
      pub.topics.some(topic => selectedTopics.includes(topic))
    );

    filteredPublications.sort((a, b) => new Date(b.date) - new Date(a.date));

    filteredPublications.forEach(pub => {
      const pubDiv = document.createElement('div');
      pubDiv.className = 'publication';

      const linksHTML = Object.entries(pub.links || {}).map(([key, url]) => {
        return `<a href="${url}" target="_blank" class="resource-link">${key}</a>`;
      }).join(' ');

      const topicsHTML = Object.entries(pub.topics || {}).map(([key, value]) => {
        return `<span class="topic">${value}</span>`;
      }).join(' ');

      pubDiv.innerHTML = `
        <div class="publication-left">
            <strong>${pub.date}</strong>
        </div>
        <div class="publication-right">
            <h3><a href="${pub.main_link || '#'}" target="_blank">${pub.title}</a></h3>
            <p>${pub.authors}</p>
            <p>${pub.venue}</p>
            <p>${pub.summary}</p>
            <div class="resource-topics">${topicsHTML}</div>
            <div class="resource-links">${linksHTML}</div>
        </div>
      `;

      container.appendChild(pubDiv);
    });
  }

  // Function to select all topics
  function selectAllTopics() {
    document.querySelectorAll('.topic-filter').forEach(el => el.classList.add('selected'));
  }
  function deselectAllTopics() {
    document.querySelectorAll('.topic-filter').forEach(el => el.classList.remove('selected'));
  }

  // Event listeners
  document.getElementById('select-all').addEventListener('click', () => {
    selectAllTopics();
    renderPublications();
  });
  document.getElementById('select-none').addEventListener('click', () => {
    deselectAllTopics();
    renderPublications();
  });

  // Initial render with all topics selected
  selectAllTopics();
  renderPublications();

</script>

<style>
  .publication {
    margin: 1rem 0;
    padding: 1rem;
    border-bottom: 1px solid #ddd;
    display: flex;
    align-items: flex-start;
    gap: 1rem;
  }
  .publication:last-child {
    border-bottom: 0px;
  }

  .publication-left {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: flex-start;
    flex-shrink: 0;
    max-width: 150px;
  }

  .publication-right {
    display: flex;
    flex-direction: column;
    flex-grow: 1;
  }

  .publication-thumbnail {
    width: 150px;
    max-height: 150px;
    object-fit: cover;
    border-radius: 10px;
  }

  .publication p, h3 {
    margin: 0px;
  }

  .resource-links, .resource-topics {
    margin: 0px;
  }

  .resource-link, .topic {
    display: inline-block;
    margin: 0 0.2rem 0 0;
    padding: 0.2rem 0.5rem;
    color: white;
    border-radius: 10px;
    text-decoration: none;
    font-size: 0.8rem;
    font-family: sans-serif;
    font-weight: bold;
  }
  .resource-link {
    background-color: #817AE4;
  }
  .resource-link:hover {
    background-color: #6660C1;
    color: white;
  }
  .resource-link:active {
    color: white;
  }

  #topic-filters {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin-bottom: 1rem;
  }

  #topic-filters p {
    margin: 0rem;
  }

  .topic-filter, .topic {
    background-color: #6791EC;
    color: white;
  }
  .topic-filter {
    padding: 0.5rem 1rem;
    border-radius: 10px;
    font-size: 0.9rem;
    font-weight: bold;
    cursor: pointer;
  }

  .topic-filter.selected {
    background-color: #1358EC;
  }
</style>
