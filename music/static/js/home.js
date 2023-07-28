/** Converts span elements for reviews into stars. */
function loadReviewsAsStars() {
    document.querySelectorAll('.reviewStarsReadOnly').forEach((e) => {
        const rating = Number(e.attributes.rating.value);

        const fullStars = new Array(rating).fill(`<span class="ratingStarFilled">★</span>`);
        const emptyStars = new Array(5 - rating).fill(`<span class="ratingStarOutlined">☆</span>`);

        e.innerHTML = fullStars.join(``) + emptyStars.join(``);
    });
}

/** Loads inner HTML of pagination bars across site. */
function loadPaginationBars() {
    function handlePageChange(oldPage, newPage) {
        if (window.location.search.includes(`?page=${oldPage}`)) {
            window.location.search = window.location.search.replace(`?page=${oldPage}`, `?page=${newPage}`);
        } else if (window.location.search.includes(`&page=${oldPage}`)) {
            window.location.search = window.location.search.replace(`&page=${oldPage}`, `&page=${newPage}`);
        } else if (window.location.search !== ``) {
            window.location.search += `&page=${newPage}`;
        } else {
            window.location.search = `?page=${newPage}`;
        }
    }

    document.querySelectorAll('.paginationBar').forEach((e) => {
        const page = Number(e.attributes.page.value);
        const numPages = Number(e.attributes.num_pages.value);

        if (numPages >= 5) {
            const btn = document.createElement(`button`);
            btn.innerText = `<<`;
            btn.onclick = () => handlePageChange(page, 1);
            btn.title = `First Page`;
            btn.disabled = page <= 1;
            e.appendChild(btn);
        }

        {
            const btn = document.createElement(`button`);
            btn.innerText = `<`;
            btn.onclick = () => handlePageChange(page, page - 1);
            btn.title = `Previous Page`;
            btn.disabled = page <= 1;
            e.appendChild(btn);
        }

        const mainText = document.createElement(`span`);
        mainText.innerText = `Page ${page} of ${numPages}`;
        e.appendChild(mainText);

        {
            const btn = document.createElement(`button`);
            btn.innerText = `>`;
            btn.onclick = () => handlePageChange(page, page + 1);
            btn.title = `Next Page`;
            btn.disabled = page >= numPages;
            e.appendChild(btn);
        }

        if (numPages >= 5) {
            const btn = document.createElement(`button`);
            btn.innerText = `>>`;
            btn.onclick = () => handlePageChange(page, numPages);
            btn.title = `Last Page`;
            btn.disabled = page >= numPages;
            e.appendChild(btn);
        }
    });
}

loadPaginationBars();
loadReviewsAsStars();
