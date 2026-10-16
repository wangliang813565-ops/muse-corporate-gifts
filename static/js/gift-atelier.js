/* Product discovery and visitor-reviewed WhatsApp briefs. No automatic transmission. */
(() => {
  'use strict';
  const studio = document.querySelector('[data-gift-studio]');
  if (!studio || !document.getElementById('gift-atelier-data')) return;
  const payload = JSON.parse(document.getElementById('gift-atelier-data').textContent);
  const copy = JSON.parse(document.getElementById('cg-copy').textContent);
  const ui = payload.ui;
  const lang = payload.language;
  const seasons = JSON.parse(document.getElementById('gift-occasion-data').textContent);
  const occasionSelect = document.getElementById('gift-occasion');
  const occasions = new Map(seasons.guides.map(g => [g.id,g]));
  const products = new Map(payload.products.map(p => [p.id, p]));
  const cards = [...studio.querySelectorAll('.vg-product')];
  const filters = [...studio.querySelectorAll('[data-filter]')];
  const addButtons = [...studio.querySelectorAll('[data-product-id]')];
  const selected = new Map();
  const search = document.getElementById('gift-search');
  const recipient = document.getElementById('gift-recipient');
  const categorySelect = document.getElementById('gift-category');
  const listBar = studio.querySelector('[data-list-bar]');
  const listItems = studio.querySelector('[data-shortlist-items]');
  const form = document.getElementById('cg-brief-form');
  const review = studio.querySelector('[data-review]');
  const message = document.getElementById('cg-message');
  const sendLink = studio.querySelector('[data-send-link]');
  const dialog = document.getElementById('gift-detail');
  const detailAdd = studio.querySelector('[data-detail-add]');
  let category = 'all';
  let detailId = null;
  let lastDialogTrigger = null;

  const title = p => `${p.brand} — ${p.title[lang]}`;
  const clean = text => text.normalize('NFKD').toLocaleLowerCase().replace(/[\u064B-\u065F]/g, '').trim();
  // Resolve assets from the site root rather than the current section URL.
  const productImage = p => new URL(`/images/corporate-gifts/v2/${p.image}`, location.origin).href;
  const brandAliases = {LAIFEN:'لافين لايفن',SHOKZ:'شوكس شوكز',HUAWEI:'هواوي',EKETOP:'إيكي توب',HOTO:'هوتو',DJI:'دي جي آي',LOFREE:'لوفري',WACACO:'واكاكو',GiiKER:'جيكر',SOUNDCORE:'ساوندكور',ANKER:'أنكر انكر',INSTA360:'إنستا انستا 360',XIAOMI:'شاومي',TIMEMORE:'تايمور',ROKR:'روكر','MUSE ATELIER':'ميوز'};
  const productKeywords = {
    'laifen-wave':'electric toothbrush dental فرشاة أسنان', 'laifen-p3':'shaver razor grooming ماكينة حلاقة',
    'shokz-openfit':'earbuds headphones open ear سماعات', 'shokz-openrun':'headphones running sports سماعات رياضة',
    'huawei-freeclip':'earbuds headphones open ear سماعات', 'soundcore-space':'headphones travel audio سماعات', 'huawei-watch':'smartwatch wearable ساعة ذكية',
    'anker-powerbank':'power bank portable charging laptop شحن باور بنك', 'anker-desktop':'desktop charger charging station شاحن مكتبي',
    'dji-mobile':'gimbal stabilizer phone camera تصوير مثبت هاتف', 'dji-pocket':'camera video creator كاميرا تصوير', 'insta360-go':'camera action travel كاميرا تصوير',
    'xiaomi-air':'car tyre tire pump compressor منفاخ إطارات', 'hoto-kit':'tools electric screwdriver أدوات مفك',
    'wacaco-pico':'espresso coffee maker manual قهوة إسبريسو', 'timemore-s3':'coffee grinder manual قهوة مطحنة',
    'eketop':'spinning top kinetic metal desk toy بلبل معدني', 'lofree':'keyboard transparent desk لوحة مفاتيح',
    'rokr-spaceport':'marble run wooden engineering model puzzle نموذج ميكانيكي', 'giiker-slide':'puzzle game family لعبة ألغاز', 'giiker-four':'board game family strategy لعبة عائلة',
    'ceramic-qahwa':'dallah finjan coffee qahwa ceramic cups دلة فناجين قهوة عربية', 'leather-folio':'leather folio cardholder executive جلد حافظة',
    'oud-majlis':'incense oud burner mabkhara architectural wind crown parapet courtyard بخور عود مبخرة برج سور فناء',
    'cnc-sculpture':'metal sculpture cnc commemorative award معدن تذكار', 'executive-desk':'leather stone desk set طقم مكتب جلد حجر',
    'woven-hospitality':'woven basket presentation hospitality case ضيافة سلة', 'glass-hospitality':'glass water carafe tumblers زجاج إبريق مياه',
    'leather-weekender':'leather travel bag weekender حقيبة سفر جلدية'
  };

  function applyFilters() {
    const query = clean(search.value);
    let count = 0;
    for (const card of cards) {
      const p = products.get(card.dataset.id);
      const haystack = clean([p.brand, brandAliases[p.brand] || '', productKeywords[p.id] || '', p.title.en, p.title.ar, p.text[lang], p.scene[lang]].join(' '));
      const personFits = recipient.value === 'all' || p.recipients.includes(recipient.value) || (recipient.value === 'guests' && ['play','crafted'].includes(p.category));
      const occasion = occasions.get(occasionSelect.value);
      const occasionFits = !occasion || occasion.products.includes(p.id);
      const show = (category === 'all' || category === p.category) && (!query || haystack.includes(query)) && personFits && occasionFits;
      card.hidden = !show;
      if (show) count++;
    }
    filters.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.filter === category)));
    categorySelect.value = category;
    studio.querySelectorAll('[data-collection]').forEach(link => {
      if (link.dataset.collection === category) link.setAttribute('aria-current','true');
      else link.removeAttribute('aria-current');
    });
    studio.querySelector('[data-result-count]').textContent = String(count);
    studio.querySelector('[data-empty]').hidden = count > 0;
    const occasion = occasions.get(occasionSelect.value);
    studio.querySelector('[data-occasion-context]').hidden = !occasion;
    if (occasion) {
      studio.querySelector('[data-occasion-heading]').textContent = `${seasons.ui.focus}: ${occasion.title[lang]}`;
      studio.querySelector('[data-occasion-answer]').textContent = occasion.answer[lang];
      studio.querySelector('[data-occasion-guide-link]').href = `#occasion-${occasion.id}`;
    }
  }
  function resetFilters() {
    category = 'all'; search.value = ''; recipient.value = 'all'; occasionSelect.value = 'all'; applyFilters();
  }
  filters.forEach(button => button.addEventListener('click', () => {category = button.dataset.filter; applyFilters();}));
  studio.querySelectorAll('[data-collection]').forEach(link => link.addEventListener('click', () => {category = link.dataset.collection; applyFilters();}));
  studio.querySelectorAll('[data-reset]').forEach(button => button.addEventListener('click', resetFilters));
  search.addEventListener('input', applyFilters);
  recipient.addEventListener('change', applyFilters);
  categorySelect.addEventListener('change', () => {category = categorySelect.value; applyFilters();});
  function chooseOccasion(id) {
    if (!occasions.has(id)) return;
    category = 'all'; search.value = ''; recipient.value = 'all'; occasionSelect.value = id;
    form.elements.occasion.value = occasions.get(id).occasion;
    applyFilters();
  }
  occasionSelect.addEventListener('change', () => {
    if (occasionSelect.value === 'all') applyFilters();
    else chooseOccasion(occasionSelect.value);
  });
  studio.querySelectorAll('[data-gift-occasion]').forEach(link => link.addEventListener('click', () => chooseOccasion(link.dataset.giftOccasion)));
  studio.querySelector('[data-occasion-guide-link]').addEventListener('click', () => {
    const guide = document.getElementById(`occasion-${occasionSelect.value}`); if (guide) guide.open = true;
  });

  function toggleProduct(id) {
    if (!products.has(id)) return;
    if (selected.has(id)) selected.delete(id);
    else selected.set(id, products.get(id));
    updateSelection();
  }
  function updateSelection() {
    listItems.replaceChildren();
    listBar.hidden = selected.size === 0;
    document.body.classList.toggle('has-gift-selection', selected.size > 0);
    studio.querySelector('[data-selected-count]').textContent = String(selected.size);
    [...selected].slice(0,3).forEach(([id,p]) => {
      const li = document.createElement('li');
      const button = document.createElement('button');
      button.type = 'button';
      button.setAttribute('aria-label', `${ui.remove}: ${title(p)}`);
      const img = document.createElement('img'); img.src = productImage(p); img.alt = ''; img.width = 40; img.height = 40;
      const name = document.createElement('span'); name.textContent = p.title[lang];
      const close = document.createElement('span'); close.textContent = '×'; close.setAttribute('aria-hidden','true');
      button.append(img,name,close); li.append(button); listItems.append(li);
      button.addEventListener('click', () => {
        selected.delete(id); updateSelection();
        const nextRemove = listItems.querySelector('button');
        if (nextRemove) nextRemove.focus();
        else document.getElementById('selection-heading').focus({preventScroll:true});
      });
    });
    if (selected.size > 3) {
      const li = document.createElement('li'); li.className = 'vg-more-selected'; li.textContent = `+${selected.size-3} ${ui.moreSelected}`; listItems.append(li);
    }
    for (const button of addButtons) {
      const active = selected.has(button.dataset.productId);
      button.setAttribute('aria-pressed', String(active));
      button.setAttribute('aria-label', `${active ? ui.remove : ui.add}: ${button.dataset.productName}`);
      button.querySelector('[data-add-label]').textContent = active ? ui.added : ui.add;
      button.querySelector('.vg-add-icon path').setAttribute('d', active ? 'M5 13l4 4L19 7' : 'M12 5v14M5 12h14');
    }
    studio.querySelector('[data-brief-selection]').textContent = selected.size ? [...selected.values()].map(title).join('\n') : ui.listEmpty;
    if (detailId) {
      detailAdd.textContent = selected.has(detailId) ? `${ui.added} ✓` : `${ui.add} +`;
      detailAdd.setAttribute('aria-pressed',String(selected.has(detailId)));
    }
    try { sessionStorage.setItem('muse-gift-list-v2', JSON.stringify([...selected.keys()])); } catch (_) { /* Selection still works without storage. */ }
    if (!review.hidden) showReview(false);
  }
  addButtons.forEach(button => button.addEventListener('click', () => toggleProduct(button.dataset.productId)));

  function openDetail(id, trigger) {
    const p = products.get(id); if (!p) return;
    detailId = id; lastDialogTrigger = trigger;
    const img = studio.querySelector('[data-detail-image]'); img.src = productImage(p); img.alt = title(p);
    const gallery = studio.querySelector('[data-detail-gallery]');
    gallery.replaceChildren(); gallery.hidden = !p.gallery?.length;
    (p.gallery || []).forEach((variant, i) => {
      const button = document.createElement('button'); button.type = 'button';
      button.setAttribute('aria-pressed', String(i === 0));
      const thumb = document.createElement('img'); thumb.src = productImage({image:variant.image.replace('.webp','-card.webp')});
      thumb.alt = ''; thumb.width = 100; thumb.height = 100;
      const label = document.createElement('span'); label.textContent = variant.label[lang];
      button.append(thumb,label); gallery.append(button);
      button.addEventListener('click', () => {
        img.src = productImage(variant); img.alt = `${title(p)} — ${variant.label[lang]}`;
        gallery.querySelectorAll('button').forEach(b => b.setAttribute('aria-pressed',String(b === button)));
      });
    });
    studio.querySelector('[data-detail-brand]').textContent = p.brand;
    document.getElementById('gift-detail-title').textContent = p.title[lang];
    studio.querySelector('[data-detail-text]').textContent = p.text[lang];
    studio.querySelector('[data-detail-scene]').textContent = p.scene[lang];
    studio.querySelector('[data-detail-personal]').textContent = p.personalise?.[lang] || (p.custom ? ui.originalCustom : ui.brandCustom);
    const notice = studio.querySelector('[data-detail-notice]'); notice.textContent = p.notice?.[lang] || ''; notice.hidden = !p.notice?.[lang];
    detailAdd.textContent = selected.has(id) ? `${ui.added} ✓` : `${ui.add} +`;
    detailAdd.setAttribute('aria-pressed',String(selected.has(id)));
    dialog.showModal(); document.body.classList.add('gift-dialog-open');
  }
  studio.querySelectorAll('[data-view]').forEach(button => button.addEventListener('click', () => openDetail(button.dataset.view,button)));
  studio.querySelector('[data-close]').addEventListener('click', () => dialog.close());
  dialog.addEventListener('click', event => {
    const rect = dialog.getBoundingClientRect();
    if (event.target === dialog && (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom)) dialog.close();
  });
  dialog.addEventListener('close', () => {document.body.classList.remove('gift-dialog-open'); detailId = null; if (lastDialogTrigger) lastDialogTrigger.focus({preventScroll:true});});
  detailAdd.addEventListener('click', () => {if (detailId) toggleProduct(detailId);});

  studio.querySelectorAll('[data-occasion]').forEach(link => link.addEventListener('click', () => {
    form.elements.occasion.value = link.dataset.occasion;
    review.hidden = true; form.hidden = false;
    if (link.dataset.editItems) {
      link.dataset.editItems.split(' ').filter(id=>products.has(id)).forEach(id=>selected.set(id,products.get(id)));
      updateSelection();
    }
  }));
  document.querySelectorAll('#site-navigation a').forEach(link => link.addEventListener('click', () => {
    document.getElementById('site-navigation').classList.remove('open');
    document.querySelector('.menu-toggle').setAttribute('aria-expanded','false');
  }));
  const now = new Date();
  form.elements.date.min = [now.getFullYear(),String(now.getMonth()+1).padStart(2,'0'),String(now.getDate()).padStart(2,'0')].join('-');
  function fieldText(name) {const field = form.elements[name]; return field.selectedOptions ? field.selectedOptions[0].textContent.trim() : field.value.trim();}
  function showReview(focus = true) {
    const fields = [[copy.occasionLabel,fieldText('occasion')],[copy.recipientLabel,fieldText('recipients')],[copy.quantityLabel,fieldText('quantity')],[copy.dateLabel,form.elements.date.value]];
    const occasion = occasions.get(occasionSelect.value);
    if (occasion) fields.unshift([seasons.ui.label,occasion.title[lang]]);
    if (fieldText('company')) fields.push([copy.companyLabel,fieldText('company')]);
    const lines = [copy.messageIntro,'',...fields.map(([label,value])=>`${label}: ${value}`),'',`${copy.selectedText}:`,selected.size ? [...selected.values()].map(p=>`• ${title(p)}`).join('\n') : copy.noProducts];
    if (fieldText('notes')) lines.push('',`${copy.notesText}: ${fieldText('notes')}`);
    lines.push('',`${copy.sourceText}: ${studio.dataset.source}`);
    const text = lines.join('\n'); message.value = text;
    const url = new URL(`https://wa.me/${studio.dataset.phone}`); url.searchParams.set('text',text); sendLink.href = url.href;
    form.hidden = true; review.hidden = false;
    if (focus) document.getElementById('cg-review-heading').focus();
  }
  form.addEventListener('submit', event => {event.preventDefault(); if (form.reportValidity()) showReview();});
  studio.querySelector('[data-edit]').addEventListener('click', () => {review.hidden = true; form.hidden = false; form.elements.occasion.focus();});
  try {const saved = JSON.parse(sessionStorage.getItem('muse-gift-list-v2') || '[]'); if (Array.isArray(saved)) saved.filter(id=>products.has(id)).forEach(id=>selected.set(id,products.get(id)));} catch (_) { /* Ignore invalid local state. */ }
  updateSelection(); applyFilters();
})();
