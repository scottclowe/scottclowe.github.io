---
layout: default
title: Publications
---

<h1>Publications</h1>

<p>For a full publications list with citation counts, please see my <a href="https://scholar.google.com/citations?user=ZFPhxuAAAAAJ">Google Scholar</a> page.</p>

<!-- Topic Filters -->
<div id="topic-filters">
  <p>Filter by topic:</p>
</div>
<button id="select-all">Select all topics</button>
<button id="select-none">Deselect all topics</button>

<!-- Highlight Controls -->
<div id="highlight-controls">
  <label class="toggle-switch">
    <input type="checkbox" id="group-highlights" checked>
    <span class="slider-toggle"></span>
    <span class="toggle-label">Group highlighted papers separately</span>
  </label>
</div>

<div id="publication-counter"></div>

<!-- Container for Highlighted Publications (when grouped) -->
<div id="highlighted-publications-section" style="display: none;">
  <h2>Highlighted Publications</h2>
  <div id="highlighted-publications-container">
    <!-- Highlighted publications will be dynamically inserted here -->
  </div>
</div>

<!-- Container for All Publications -->
<div id="all-publications-section">
  <h2 id="all-publications-header">Publications</h2>
  <div id="publications-container">
    <!-- Publications will be dynamically inserted here -->
  </div>
</div>

<!-- JavaScript for Interactivity -->
<script>
  // Publications data from YAML (inserted by Jekyll)
  const publicationsRaw = {{ site.data.publications | jsonify }};

  // Add original index to each publication for sorting
  const publications = publicationsRaw.map((pub, index) => ({
    ...pub,
    originalIndex: index
  }));

  // Separate highlighted and non-highlighted publications
  const highlightedPublications = publications
    .filter(pub => pub.highlighted !== undefined && pub.highlighted !== null)
    .sort((a, b) => a.highlighted - b.highlighted); // Sort by highlighted value (ascending)

  const otherPublications = publications
    .filter(pub => pub.highlighted === undefined || pub.highlighted === null);

  // Count topic occurrences
  const topicCounts = {};
  publications.forEach(pub => {
    pub.topics.forEach(topic => {
      topicCounts[topic] = (topicCounts[topic] || 0) + 1;
    });
  });

  // Sort topics by frequency (most to least)
  const sortedTopics = Object.keys(topicCounts).sort((a, b) => topicCounts[b] - topicCounts[a]);

  // Populate the topic filters
  const topicFilters = document.getElementById('topic-filters');

  sortedTopics.forEach(topic => {
    const topicElement = document.createElement('div');
    topicElement.className = 'topic-filter selected';
    topicElement.textContent = `${topic} (${topicCounts[topic]})`;
    topicElement.dataset.topic = topic;

    topicElement.addEventListener('click', () => {
      topicElement.classList.toggle('selected');
      renderPublications();
    });

    topicFilters.appendChild(topicElement);
  });

  // Function to update publication counter
  function updatePublicationCounter(displayedCount, highlightedCount, numFilters, isGrouped) {
    const totalCount = publications.length;
    const counterElement = document.getElementById('publication-counter');

    if (counterElement) {
      if (numFilters == 0) {
        counterElement.textContent = '';
      }
      else {
        const parts = [];
        if (highlightedCount > 0 && isGrouped) {
          parts.push(`${highlightedCount} highlighted`);
        }
        parts.push(`${displayedCount} of ${totalCount} total`);
        counterElement.textContent = `Showing ${parts.join(', ')}`;
      }
    }
  }

  // Function to render a single publication
  function renderPublication(pub, isHighlighted = false, showBorder = true) {
    const selectedTopics = Array.from(document.querySelectorAll('.topic-filter.selected'))
      .map(el => el.dataset.topic);

    const pubDiv = document.createElement('div');
    let className = 'publication';
    if (isHighlighted) {
      className += ' highlighted-publication';
    }
    if (showBorder) {
      className += ' with-border';
    }
    pubDiv.className = className;

    const linksHTML = Object.entries(pub.links || {}).map(([key, url]) => {
      return `<a href="${url}" target="_blank" class="resource-link">${key}</a>`;
    }).join(' ');

    const topicsHTML = Object.entries(pub.topics || {}).map(([key, value]) => {
      var extra_class = selectedTopics.includes(value) ? "selected" : "";
      return `<span class="topic ${extra_class}">${value}</span>`;
    }).join(' ');

    pubDiv.innerHTML = `
      <div class="publication-left">
          <strong>${pub.date}</strong>
      </div>
      <div class="publication-right">
          <h3><a href="${pub.main_link || '#'}" target="_blank">${pub.title}</a></h3>
          <p>${pub.authors.replace(/\s/g, '&nbsp;').replace(/,&nbsp;/g, ', ').replace(/†/g, '<sup>†</sup>')}</p>
          <p><i>${pub.venue}</i></p>
          <p>${pub.summary}</p>
          <div class="resource-topics">${topicsHTML}</div>
          <div class="resource-links">${linksHTML}</div>
      </div>
    `;

    return pubDiv;
  }

  // Function to render publications
  function renderPublications() {
    const selectedTopics = Array.from(document.querySelectorAll('.topic-filter.selected'))
      .map(el => el.dataset.topic);

    let shownTopics = selectedTopics;
    if (shownTopics.length == 0) {
        shownTopics = Array.from(document.querySelectorAll('.topic-filter'))
            .map(el => el.dataset.topic);
    }

    const isGrouped = document.getElementById('group-highlights').checked;

    // Filter highlighted publications
    const filteredHighlightedPublications = highlightedPublications.filter(pub =>
      pub.topics.some(topic => shownTopics.includes(topic))
    );

    // Filter other publications
    const filteredOtherPublications = otherPublications.filter(pub =>
      pub.topics.some(topic => shownTopics.includes(topic))
    );

    if (isGrouped) {
      // Render highlighted publications section
      const highlightedContainer = document.getElementById('highlighted-publications-container');
      const highlightedSection = document.getElementById('highlighted-publications-section');
      highlightedContainer.innerHTML = '';

      if (filteredHighlightedPublications.length > 0) {
        highlightedSection.style.display = 'block';
        filteredHighlightedPublications.forEach(pub => {
          highlightedContainer.appendChild(renderPublication(pub, true, false));
        });
      } else {
        highlightedSection.style.display = 'none';
      }

      // Render other publications sorted by date
      const container = document.getElementById('publications-container');
      container.innerHTML = '';

      filteredOtherPublications.sort((a, b) => new Date(b.date) - new Date(a.date));
      filteredOtherPublications.forEach(pub => {
        container.appendChild(renderPublication(pub, false, true));
      });

      // Update header text
      const allPubsHeader = document.getElementById('all-publications-header');
      if (filteredHighlightedPublications.length > 0) {
        allPubsHeader.textContent = 'All Publications';
      } else {
        allPubsHeader.textContent = 'Publications';
      }
    } else {
      // Hide the separate highlighted section
      document.getElementById('highlighted-publications-section').style.display = 'none';

      // Merge all publications and sort: highlighted by original order, others by date, then interleave by original index
      const allFilteredPublications = [
        ...filteredHighlightedPublications,
        ...filteredOtherPublications
      ].sort((a, b) => {
        // Sort by original document order (which is chronological)
        return a.originalIndex - b.originalIndex;
      });

      // Render all publications together
      const container = document.getElementById('publications-container');
      container.innerHTML = '';

      allFilteredPublications.forEach(pub => {
        const isHighlighted = pub.highlighted !== undefined && pub.highlighted !== null;
        container.appendChild(renderPublication(pub, isHighlighted, true));
      });

      // Update header text
      document.getElementById('all-publications-header').textContent = 'Publications';
    }

    // Update the counter
    const totalDisplayed = filteredHighlightedPublications.length + filteredOtherPublications.length;
    updatePublicationCounter(totalDisplayed, filteredHighlightedPublications.length, selectedTopics.length, isGrouped);
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
  document.getElementById('group-highlights').addEventListener('change', renderPublications);

  // Initial render with all topics selected
  deselectAllTopics();
  renderPublications();

</script>

<style>
  button {
    padding: 0.4em 0.8em;
    border-radius: 100vw;
  }

  .publication {
    padding-left: 1rem;
    padding-right: 1rem;
    padding-top: 0.5rem;
    padding-bottom: 0.5rem;
    margin-top: 0.5rem;
    margin-bottom: 0.5rem;
    display: flex;
    align-items: flex-start;
    gap: 1rem;
    position: relative;
  }

  /* Add separator line below highlighted publications in grouped together mode */
  .publication.with-border::after {
    content: '';
    position: absolute;
    left: 0;
    right: 0;
    bottom: -0.5rem; /* Position it halfway in the margin space */
    height: 1px;
    background-color: #ddd;
  }
  .publication.with-border:last-child::after {
    height: 0px;
  }

  .highlighted-publication {
    background-color: #f0f8ff; /* Pale blue background */
    border-radius: 8px;
  }

  /* Highlighted publications without border get margin for spacing */
  .highlighted-publication:not(.with-border) {
    padding-top: 1rem;
    padding-bottom: 1rem;
  }

  /* Highlighted publications with border (grouped together mode) */
  .highlighted-publication.with-border {
    margin-top: 1rem;
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
    background-color: #967AE4;
  }
  .resource-link:hover {
    background-color: #5932C3;
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

  .topic-filter.selected, .topic.selected {
    background-color: #1358EC;
  }

  #highlighted-publications-section {
    margin-bottom: 2rem;
  }

  #highlighted-publications-section h2,
  #all-publications-section h2 {
    margin-top: 2rem;
    margin-bottom: 1rem;
  }

  /* Toggle switch styles */
  #highlight-controls {
    margin: 1rem 0;
  }

  .toggle-switch {
    display: inline-flex;
    align-items: center;
    cursor: pointer;
    user-select: none;
  }

  .toggle-switch input[type="checkbox"] {
    display: none;
  }

  .slider-toggle {
    position: relative;
    display: inline-block;
    width: 50px;
    height: 24px;
    background-color: #ccc;
    border-radius: 24px;
    transition: background-color 0.3s;
    margin-right: 0.5rem;
  }

  .slider-toggle::before {
    content: '';
    position: absolute;
    width: 18px;
    height: 18px;
    left: 3px;
    top: 3px;
    background-color: white;
    border-radius: 50%;
    transition: transform 0.3s;
  }

  .toggle-switch input[type="checkbox"]:checked + .slider-toggle {
    background-color: #1358EC;
  }

  .toggle-switch input[type="checkbox"]:checked + .slider-toggle::before {
    transform: translateX(26px);
  }

  .toggle-label {
    font-size: 0.95rem;
    font-weight: 500;
  }
</style>
