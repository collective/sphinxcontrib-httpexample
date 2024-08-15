document.addEventListener("DOMContentLoaded", function() {
  // Select all elements with the class 'http-example container'
  var containers = document.querySelectorAll('.http-example.container');
  containers.forEach(function(container) {

    // Get all child elements
    var blocks = Array.from(container.children);

    // Find caption elements or derive them from elements with the 'caption-text' class
    var captions = container.querySelectorAll('.caption');
    if (captions.length === 0) {
      captions = container.querySelectorAll('.caption-text');
      captions.forEach(function(caption) {
        caption.classList.add('caption');
      });
    } else {
      captions = Array.from(captions);
    }

    // Process each caption element
    captions.forEach(function(caption) {
      var orphan, block = !!caption.parentElement.id ? caption.parentElement : caption.parentElement.parentElement;
      block.setAttribute('role', 'tabpanel');
      block.setAttribute('tabindex', '0');
      block.setAttribute('aria-labelledby', block.id + '-label');

      caption.id = block.id + '-label';
      caption.setAttribute('role', 'tab');
      caption.setAttribute('tabindex', '0');
      caption.setAttribute('aria-label', caption.textContent.trim());
      caption.setAttribute('aria-controls', block.id);

      // Click event for captions
      caption.addEventListener('click', function() {
        // Deselect other captions
        captions.forEach(function(otherCaption) {
          otherCaption.setAttribute('aria-selected', 'false');
          otherCaption.classList.remove('selected');
        });

        // Select the clicked caption
        caption.setAttribute('aria-selected', 'true');
        caption.classList.add('selected');

        // Hide other blocks and show the selected one
        blocks.forEach(function(otherBlock) {
          if (otherBlock !== block) {
            otherBlock.style.display = 'none';
            otherBlock.setAttribute('hidden', 'hidden');
          }
        });
        block.style.display = '';
        block.removeAttribute('hidden');
      });

      // Keydown event for accessibility
      caption.addEventListener('keydown', function(event) {
        if (event.code === 'Space' || event.code === 'Enter') {
          caption.click();
        }
      });

      if (caption.classList.contains("caption-text")) {
        orphan = caption.parentElement;
        container.appendChild(caption);
        orphan.remove();
      } else {
        container.appendChild(caption);
      }
    });

    // Set ARIA role for the container
    container.setAttribute('role', 'tablist');

    // Append blocks back to the container
    blocks.forEach(function(block) {
      container.appendChild(block);
    });

    // Automatically click the first caption to set the initial state
    if (captions.length > 0) {
      captions[0].click();
    }
  });
});
