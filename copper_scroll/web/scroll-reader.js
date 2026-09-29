/* The scroll reader: the column strip, the facing Hebrew and English lines, and
   the panel that shows a word's meaning and the editions' readings.
   Data: scroll-text.js (the Hebrew, CC BY-NC 4.0) and scroll-notes.js (the
   translation, glosses, notes and entries written for this project). */
(function () {
  'use strict';
  var T = window.SCROLL_TEXT, N = window.SCROLL_NOTES;
  var rowsEl = document.getElementById('rows');
  if (!T || !N || !rowsEl) {
    if (rowsEl) rowsEl.innerHTML = '<p class="small">The text files did not load. Reload the page to try again.</p>';
    return;
  }
  var ROMAN = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII'];
  var REPO = 'https://github.com/quadrin/AncientHebrewTexts/blob/main/copper_scroll/';
  var strip = document.getElementById('strip');
  var panel = document.getElementById('panel');
  var titleEl = document.getElementById('col-title');
  var metaEl = document.getElementById('col-meta');
  var prevBtn = document.getElementById('col-prev');
  var nextBtn = document.getElementById('col-next');

  function esc(s) {
    return String(s).replace(/[&<>"]/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c];
    });
  }

  /* ---- indexes ---- */
  var cols = T.columns.map(function (c) { return { n: c.c, r: ROMAN[c.c - 1], lines: c.lines }; });
  var lineWords = {};          // "I 1" -> words
  var lineCol = {};            // "I 1" -> column index
  var order = [];              // every "line#word" in text order
  cols.forEach(function (c, ci) {
    c.lines.forEach(function (l) {
      var key = c.r + ' ' + l.l;
      lineWords[key] = l.w;
      lineCol[key] = ci;
      l.w.forEach(function (w, i) { order.push(key + '#' + i); });
    });
  });
  var pos = {};
  order.forEach(function (k, i) { pos[k] = i; });

  var byWord = {}, byLemma = {};
  Object.keys(N.notes).forEach(function (id) {
    var n = N.notes[id];
    n.at.forEach(function (spot) {
      spot[1].forEach(function (i) { (byWord[spot[0] + '#' + i] = byWord[spot[0] + '#' + i] || []).push(id); });
    });
    (n.lemma || []).forEach(function (lx) { (byLemma[lx] = byLemma[lx] || []).push(id); });
  });

  // which entry each word belongs to
  var entries = N.entries, entryById = {}, wordEntry = {};
  entries.forEach(function (e) {
    entryById[e.id] = e;
    e.from = pos[e.start + '#' + (e.startWord || 0)];
  });
  var sorted = entries.slice().sort(function (a, b) { return a.from - b.from; });
  sorted.forEach(function (e, i) {
    var to = i + 1 < sorted.length ? sorted[i + 1].from : order.length;
    e.to = to;
    for (var p = e.from; p < to; p++) wordEntry[order[p]] = e.id;
  });
  function entryLines(e) {
    var seen = {}, out = [];
    for (var p = e.from; p < e.to; p++) {
      var ln = order[p].split('#')[0];
      if (!seen[ln]) { seen[ln] = 1; out.push(ln); }
    }
    return out;
  }

  function notesFor(key) {
    var ids = (byWord[key] || []).slice();
    var w = wordAt(key);
    (w && w.m || []).forEach(function (m) {
      (byLemma[m[1]] || []).forEach(function (id) { if (ids.indexOf(id) < 0) ids.push(id); });
    });
    return ids;
  }
  function wordAt(key) {
    var p = key.split('#');
    return (lineWords[p[0]] || [])[+p[1]];
  }

  /* ---- rendering the Hebrew ---- */
  var CLS = { r: 's-r', u: 's-u', x: 's-x', d: 's-d', c: 's-c', s: 's-s', g: 's-g' };
  var WRAP = { r: ['[', ']'], x: ['{', '}'], d: ['{{', '}}'], c: ['⟨', '⟩'] };
  function segHtml(seg) {
    var t = esc(seg[0]), k = seg[1];
    if (!k) return t;
    var w = WRAP[k];
    return '<span class="' + CLS[k] + '"' + (k === 'g' ? ' lang="grc"' : '') + '>' + (w ? w[0] + t + w[1] : t) + '</span>';
  }
  function plainWord(w) {
    return w.h.map(function (s) { return s[1] === 'x' || s[1] === 'd' ? '' : s[0]; }).join('');
  }
  function wordHtml(key, w) {
    var cls = 'w', inner;
    if (w.n != null) {
      cls += ' num';
      inner = w.n + (w.h.length ? ' ' + w.h.map(segHtml).join('') : '');
    } else if (w.greek) {
      inner = '<span class="greek" lang="grc">' + esc(plainWord(w)) + '</span>';
    } else {
      inner = w.h.map(segHtml).join('');
    }
    if (notesFor(key).length) cls += ' has-note';
    var label = w.n != null ? 'numeral ' + w.n : plainWord(w);
    return '<button type="button" class="' + cls + '" data-k="' + key + '" aria-label="' + esc(label) + '">' + inner + '</button>';
  }

  function enHtml(key) {
    return (N.tr[key] || []).map(function (s) {
      if (typeof s === 'string') return esc(s);
      return '<button type="button" class="nt" data-note="' + esc(s[1]) + '">' + esc(s[0]) + '</button>';
    }).join('');
  }

  function range(e) {
    if (e.end === e.start) return e.start;
    var a = e.start.split(' '), b = e.end.split(' ');
    return a[0] === b[0] ? e.start + '–' + b[1] : e.start + '–' + e.end;
  }
  function statusText(e) {
    if (e.status === 'best-supported') return e.place;
    if (e.status === 'possible only') return e.possible.length ? 'possible: ' + e.possible.join('; ') : 'possible places only';
    return 'no place identified';
  }
  function chip(e) {
    if (e.status === 'best-supported') return '<span class="chip ' + esc(e.conf) + '">' + esc(e.conf) + '</span>';
    if (e.status === 'possible only') return '<span class="chip poss">possible</span>';
    return '';
  }

  /* ---- the strip ---- */
  function buildStrip() {
    var html = '';
    cols.forEach(function (c, ci) {
      if (ci === 4 || ci === 8) html += '<span class="seam" aria-hidden="true"></span>';
      var mini = c.lines.map(function (l) {
        return '<div>' + esc(l.w.map(function (w) { return w.n != null ? '·' : plainWord(w); }).join(' ')) + '</div>';
      }).join('');
      html += '<button type="button" class="sheet-col" data-col="' + ci + '" aria-label="Column ' + c.r + '">' +
        '<span class="cn">' + c.r + '</span><div class="mini" aria-hidden="true">' + mini + '</div></button>';
    });
    strip.innerHTML = html;
  }

  /* ---- a column ---- */
  var current = -1;
  function showColumn(ci, opts) {
    opts = opts || {};
    if (ci < 0 || ci >= cols.length) return;
    current = ci;
    var c = cols[ci];
    var first = c.r + ' ' + c.lines[0].l, last = c.r + ' ' + c.lines[c.lines.length - 1].l;
    var ents = entries.filter(function (e) {
      return e.from <= pos[last + '#' + (lineWords[last].length - 1)] && e.to > pos[first + '#0'];
    });
    titleEl.textContent = 'Column ' + c.r;
    metaEl.textContent = 'lines 1–' + c.lines.length + ' · entries ' + ents[0].id + '–' + ents[ents.length - 1].id;
    prevBtn.disabled = ci === 0;
    nextBtn.disabled = ci === cols.length - 1;
    prevBtn.textContent = ci > 0 ? '← Column ' + cols[ci - 1].r : '← Previous';
    nextBtn.textContent = ci < cols.length - 1 ? 'Column ' + cols[ci + 1].r + ' →' : 'Next →';

    var html = '';
    c.lines.forEach(function (l) {
      var key = c.r + ' ' + l.l;
      entries.forEach(function (e) {
        if (e.start === key) {
          html += '<div class="ent"><button type="button" class="ent-btn" data-entry="' + esc(e.id) + '">' +
            '<span class="eno">Entry ' + esc(e.id) + ' · ' + esc(range(e)) + '</span>' +
            '<span class="eti">' + esc(e.title || 'Entry ' + e.id) + '</span> ' + chip(e) +
            '<span class="epl">' + esc(statusText(e)) + (e.startWord ? ' · begins in the middle of the line' : '') + '</span></button></div>';
        }
      });
      // entries that start before this column and run into it
      if (l === c.lines[0]) {
        var run = entries.filter(function (e) { return e.from < pos[key + '#0'] && e.to > pos[key + '#0']; })[0];
        if (run && run.start !== key) {
          html += '<div class="ent"><button type="button" class="ent-btn" data-entry="' + esc(run.id) + '">' +
            '<span class="eno">Entry ' + esc(run.id) + ', continued from ' + esc(run.start) + '</span>' +
            '<span class="eti">' + esc(run.title || '') + '</span></button></div>';
        }
      }
      var he = l.w.map(function (w, i) {
        var k = key + '#' + i, pre = '';
        var e = wordEntry[k];
        if (i > 0 && e && wordEntry[key + '#' + (i - 1)] !== e) pre = '<span class="midmark" title="Entry ' + esc(e) + ' begins here">' + esc(e) + '</span>';
        return pre + wordHtml(k, w);
      }).join(' ');
      html += '<div class="row" id="L-' + key.replace(' ', '-') + '" data-line="' + key + '">' +
        '<span class="en" lang="en">' + enHtml(key) + '</span>' +
        '<span class="no"><a href="#L-' + key.replace(' ', '-') + '" aria-label="Line ' + key + '">' + l.l + '</a></span>' +
        '<span class="hb" lang="he" dir="rtl">' + he + '</span></div>';
    });
    rowsEl.innerHTML = html;
    Array.prototype.forEach.call(strip.querySelectorAll('.sheet-col'), function (b) {
      b.setAttribute('aria-current', +b.dataset.col === ci ? 'true' : 'false');
    });
    var active = strip.querySelector('.sheet-col[aria-current="true"]');
    if (active && active.scrollIntoView && !opts.noStripScroll) {
      var sr = strip.getBoundingClientRect(), ar = active.getBoundingClientRect();
      if (ar.left < sr.left || ar.right > sr.right) strip.scrollLeft += ar.left - sr.left - (sr.width - ar.width) / 2;
    }
    if (!opts.keepHash) setHash('col-' + c.r);
  }

  function setHash(h) {
    if (history.replaceState) history.replaceState(null, '', '#' + h);
  }

  /* ---- highlighting ---- */
  function clearMarks() {
    Array.prototype.forEach.call(rowsEl.querySelectorAll('.on,.sel,.inent'), function (el) {
      el.classList.remove('on', 'sel', 'inent');
    });
  }
  function markWords(spots) {
    spots.forEach(function (spot) {
      spot[1].forEach(function (i) {
        var b = rowsEl.querySelector('.w[data-k="' + spot[0] + '#' + i + '"]');
        if (b) b.classList.add('on');
      });
    });
  }
  function goTo(lineKey) {
    if (lineCol[lineKey] !== current) showColumn(lineCol[lineKey], { keepHash: true });
  }
  function scrollToRow(lineKey) {
    var row = document.getElementById('L-' + lineKey.replace(' ', '-'));
    if (!row) return;
    var r = row.getBoundingClientRect();
    if (r.top < 60 || r.bottom > window.innerHeight * (window.innerWidth <= 900 ? 0.36 : 0.9)) {
      row.scrollIntoView({ block: window.innerWidth <= 900 ? 'start' : 'center', behavior: 'smooth' });
    }
  }

  /* ---- the panel ---- */
  function openPanel(html) {
    panel.innerHTML = html;
    panel.classList.add('open');
    panel.scrollTop = 0;
  }
  function closePanel() {
    panel.classList.remove('open');
  }
  var SIGLA = {
    r: 'Letters in square brackets are lost and restored by the editor.',
    u: 'Letters with a circle above are damaged; the reading is not certain.',
    x: 'Letters in braces are struck out by the editor as an engraver\'s error.',
    d: 'Letters in double braces were cancelled on the scroll itself.',
    c: 'Letters in angle brackets are supplied or corrected by the editor.',
    s: 'A raised letter is written above the line on the scroll.'
  };
  function noteHtml(id, shownKeys) {
    var n = N.notes[id];
    if (!n) return '';
    var shown = '';
    if (n.at.length) {
      shown = n.at.map(function (spot) {
        return spot[1].map(function (i) { var w = lineWords[spot[0]][i]; return w ? (w.n != null ? String(w.n) : plainWord(w)) : ''; }).join(' ');
      }).join(' … ');
    }
    var rows = '';
    if (shown) rows += '<div class="rdg shown"><div class="rdg-who">Text shown <span class="pg">Abegg, ETCBC</span></div><div class="rdg-he" lang="he" dir="rtl">' + esc(shown) + '</div><div class="rdg-mean"></div></div>';
    (n.readings || []).forEach(function (r) {
      rows += '<div class="rdg"><div class="rdg-who">' + esc(r.who) + (r.ref ? ' <span class="pg">' + esc(r.ref) + '</span>' : '') + '</div>' +
        '<div class="rdg-he" lang="he" dir="rtl">' + esc(r.reading || '') + '</div><div class="rdg-mean">' + esc(r.meaning || '') + '</div></div>';
    });
    var src = (n.src || []).map(function (f) {
      return '<a href="' + REPO + esc(f) + '">' + esc(f.split('/').pop()) + '</a>';
    }).join(', ');
    var where = n.at.length ? n.at.map(function (s) { return s[0]; }).join(', ') : '';
    return '<section class="pn-note" data-note="' + esc(id) + '"><h4>' + esc(n.label || id) + '</h4>' +
      (where ? '<p class="pn-src">' + esc(where) + (n.entry ? ' · entry ' + esc(n.entry) : '') + '</p>' : '') +
      (rows ? '<div class="rdgs" role="list" aria-label="Readings">' + rows + '</div>' : '') +
      (n.note ? '<p>' + esc(n.note) + '</p>' : '') +
      (src ? '<p class="pn-src">Research files: ' + src + '</p>' : '') + '</section>';
  }
  function entryHtml(e, brief) {
    if (!e) return '';
    var place = e.status === 'best-supported'
      ? '<p><b>Best-supported place:</b> ' + esc(e.place) + ' ' + chip(e) + '</p>'
      : e.status === 'possible only'
        ? '<p><b>Possible places only:</b> ' + esc(e.possible.join('; ') || 'none named') + '</p>'
        : '<p><b>No place identified.</b></p>';
    var html = '<h4>Entry ' + esc(e.id) + (e.title ? ': ' + esc(e.title) : '') + '</h4>' +
      '<p class="pn-src">' + esc(range(e)) + ' · Lefkovits item ' + esc(e.lef) + ' · Milik item ' + esc(String(e.milik).replace(/ \(.*?\)/g, '')) + '</p>' +
      (e.desc ? '<p>' + esc(e.desc) + '</p>' : '') + place;
    if (!brief) {
      if (e.evidence) html += '<p><b>Evidence.</b> ' + esc(e.evidence) + '</p>';
      if (e.caution) html += '<p><b>Caution.</b> ' + esc(e.caution) + '</p>';
      if (e.n) html += '<p class="pn-src">' + esc(e.n) + ' proposals on record for this entry.</p>';
    }
    html += '<div class="pn-links"><a href="../atlas-site/#entry-' + esc(e.id) + '">Open in the atlas</a>' +
      '<button type="button" data-goto-entry="' + esc(e.id) + '">Show in the text</button>' +
      '<button type="button" data-table-entry="' + esc(e.id) + '">Show in the table of entries</button></div>';
    return html;
  }
  function top(ref) {
    return '<div class="pn-top"><span class="pn-ref">' + esc(ref) + '</span><button type="button" class="pn-close" aria-label="Close">Close</button></div>';
  }

  function showWord(key) {
    var w = wordAt(key);
    if (!w) return;
    var p = key.split('#'), line = p[0];
    clearMarks();
    var btn = rowsEl.querySelector('.w[data-k="' + key + '"]');
    if (btn) btn.classList.add('on');
    var row = document.getElementById('L-' + line.replace(' ', '-'));
    if (row) row.classList.add('sel');
    var html = top(line + ' · word ' + (+p[1] + 1) + (wordEntry[key] ? ' · entry ' + wordEntry[key] : ''));
    if (w.n != null) {
      html += '<div class="pn-word num">' + w.n + '</div>' +
        '<p>A numeral written with signs, not letters. In this transcription the signs are ' + esc(w.ns.split('+').join(' + ')) +
        ' (a stroke is 1; the other signs are 10, 20 and 100). Where the editions count the signs differently, a note below says so.</p>';
      if (w.h.length) html += '<p>It is followed by <span class="legend-he" lang="he">' + esc(plainWord(w)) + '</span>, taken in this transcription as an abbreviation for “half”.</p>';
    } else {
      html += '<div class="pn-word" lang="' + (w.greek ? 'grc' : 'he') + '">' + w.h.map(segHtml).join('') + '</div>';
      var kinds = {};
      w.h.forEach(function (s) { if (SIGLA[s[1]]) kinds[s[1]] = 1; });
      Object.keys(kinds).forEach(function (k) { html += '<p class="pn-src">' + SIGLA[k] + '</p>'; });
      if (w.greek) {
        html += '<p>Greek letters engraved at the end of an entry. Seven such groups stand in columns I–IV. See <a href="#greek">The Greek letters</a> below for the readings and the tests of every explanation.</p>';
      } else if (w.m && w.m.length) {
        html += '<div class="tablebox"><table><thead><tr><th>Part</th><th>Dictionary form</th><th>Meaning</th></tr></thead><tbody>' +
          w.m.map(function (m) {
            return '<tr><td class="hbc" lang="he">' + esc(m[0]) + '</td><td class="hbc" lang="he">' + esc(m[1].replace(/_\d+$/, '').trim()) + '</td><td>' + esc(N.gloss[m[1]] || '') + '</td></tr>';
          }).join('') + '</tbody></table></div>';
      }
    }
    var ids = notesFor(key);
    ids.forEach(function (id) { html += noteHtml(id); });
    if (!ids.length && !w.greek) html += '<p class="pn-src">The editions are not reported to differ on this word.</p>';
    var tr = (N.tr[line] || []).map(function (s) { return typeof s === 'string' ? s : s[0]; }).join('');
    html += '<h4>Line ' + esc(line) + '</h4><p>' + esc(tr) + '</p>';
    if (wordEntry[key]) html += '<div class="pn-note">' + entryHtml(entryById[wordEntry[key]], true) + '</div>';
    openPanel(html);
  }

  // the place a note is shown at: the line it was selected on, else a place in
  // the column already open, else its first place
  function noteLine(n, fromLine) {
    var lines = n.at.map(function (s) { return s[0]; });
    if (fromLine && lines.indexOf(fromLine) >= 0) return fromLine;
    for (var i = 0; i < lines.length; i++) if (lineCol[lines[i]] === current) return lines[i];
    return lines[0];
  }
  function showNote(id, fromLine) {
    var n = N.notes[id];
    if (!n) return null;
    var line = noteLine(n, fromLine);
    if (line) goTo(line);
    clearMarks();
    markWords(n.at);
    Array.prototype.forEach.call(rowsEl.querySelectorAll('.nt[data-note="' + id + '"]'), function (b) { b.classList.add('on'); });
    if (line) {
      var row = document.getElementById('L-' + line.replace(' ', '-'));
      if (row) row.classList.add('sel');
    }
    var e = n.entry && entryById[n.entry];
    var head = line ? line : 'Recurs throughout';
    if (!n.entry && n.at.length > 1) head = n.at.map(function (s) { return s[0]; }).join(', ');
    openPanel(top(head + (n.entry ? ' · entry ' + n.entry : '')) + noteHtml(id) +
      (e ? '<div class="pn-note">' + entryHtml(e, true) + '</div>' : ''));
    return line;
  }

  function showEntry(id, scroll) {
    var e = entryById[id];
    if (!e) return;
    goTo(e.start);
    clearMarks();
    entryLines(e).forEach(function (ln) {
      var row = document.getElementById('L-' + ln.replace(' ', '-'));
      if (row) row.classList.add('inent');
    });
    var list = [];
    for (var p = e.from; p < e.to; p++) notesFor(order[p]).forEach(function (nid) { if (list.indexOf(nid) < 0) list.push(nid); });
    var html = top('Entry ' + e.id) + entryHtml(e, false);
    if (list.length) {
      html += '<h4>Readings that differ in this entry</h4><ul class="plain">' + list.map(function (nid) {
        return '<li><button type="button" class="nt" data-note="' + esc(nid) + '">' + esc(N.notes[nid].label || nid) + '</button></li>';
      }).join('') + '</ul>';
    }
    openPanel(html);
    if (scroll) scrollToRow(e.start);
    setHash('entry-' + e.id);
  }

  function showLine(line) {
    clearMarks();
    var row = document.getElementById('L-' + line.replace(' ', '-'));
    if (row) row.classList.add('sel');
    var list = [];
    (lineWords[line] || []).forEach(function (w, i) {
      notesFor(line + '#' + i).forEach(function (nid) { if (list.indexOf(nid) < 0) list.push(nid); });
    });
    var e = entryById[wordEntry[line + '#0']];
    var html = top('Line ' + line) + '<p class="pn-src">Select a Hebrew word for its meaning.</p>';
    list.forEach(function (nid) { html += noteHtml(nid); });
    if (e) html += '<div class="pn-note">' + entryHtml(e, true) + '</div>';
    openPanel(html);
  }

  function helpHtml() {
    return '<div class="pn-help"><h4>How to read the text</h4><ul>' +
      '<li>Select a <b>Hebrew word</b> for its parts, their meanings, and the editions\' readings.</li>' +
      '<li>Select an <b>underlined phrase</b> in the translation to see the other ways it has been read.</li>' +
      '<li>Select an <b>entry heading</b> for the place the entry names and how well it is identified.</li>' +
      '<li>A number in a box, such as <span class="w num" aria-hidden="true">17</span>, is written on the scroll with numeral signs.</li></ul>' +
      '<p>Two words recur in almost every entry and are read in different ways throughout. <button type="button" class="nt" data-note="g-kk">ככ, “talents”</button> and <button type="button" class="nt" data-note="g-dema">כלי דמע, “vessels of offering”</button>.</p>' +
      '<p class="pn-src">Entry numbers follow Puech (2006). The translation follows the Hebrew text shown, which draws mainly on Milik\'s edition; the notes give other editions\' readings where they differ.</p></div>';
  }

  /* ---- events ---- */
  strip.addEventListener('click', function (ev) {
    var b = ev.target.closest('.sheet-col');
    if (!b) return;
    showColumn(+b.dataset.col, { noStripScroll: true });
    panel.innerHTML = helpHtml();
    closePanel();
  });
  prevBtn.addEventListener('click', function () { showColumn(current - 1); });
  nextBtn.addEventListener('click', function () { showColumn(current + 1); });
  var lastFocus = null;
  document.getElementById('text').addEventListener('click', function (ev) {
    var t = ev.target;
    // a keyboard press has no pointer detail: take the reader to the panel it opened
    if (ev.detail === 0 && !panel.contains(t) && t.closest('.w, .nt, .ent-btn, .row .en')) {
      lastFocus = t.closest('button') || null;
      setTimeout(function () { panel.focus(); }, 0);
    }
    var w = t.closest('.w[data-k]');
    if (w) { showWord(w.dataset.k); return; }
    var nt = t.closest('.nt[data-note]');
    if (nt) {
      var row = nt.closest('.row');
      var shownAt = showNote(nt.dataset.note, row ? row.dataset.line : null);
      if (panel.contains(nt) && shownAt) scrollToRow(shownAt);
      return;
    }
    var eb = t.closest('[data-entry]');
    if (eb && !panel.contains(eb)) { showEntry(eb.dataset.entry); return; }
    var ge = t.closest('[data-goto-entry]');
    if (ge) { showEntry(ge.dataset.gotoEntry, true); return; }
    var te = t.closest('[data-table-entry]');
    if (te) { openTableEntry(te.dataset.tableEntry); return; }
    if (t.closest('.pn-close')) { closePanel(); if (lastFocus && document.contains(lastFocus)) lastFocus.focus(); return; }
    var en = t.closest('.row .en');
    if (en) showLine(en.parentNode.dataset.line);
  });
  document.addEventListener('keydown', function (ev) {
    if (ev.key === 'Escape' && panel.classList.contains('open')) {
      closePanel();
      if (lastFocus && document.contains(lastFocus)) lastFocus.focus();
    }
  });

  function openTableEntry(id) {
    var det = document.querySelector('details');
    var rows = document.querySelectorAll('details tbody tr');
    for (var i = 0; i < rows.length; i++) {
      var td = rows[i].querySelector('td.num');
      if (td && td.textContent.trim() === id) {
        if (det) det.open = true;
        closePanel();
        rows[i].scrollIntoView({ block: 'center', behavior: 'smooth' });
        rows[i].classList.remove('flash'); void rows[i].offsetWidth; rows[i].classList.add('flash');
        return;
      }
    }
  }

  // entry numbers in the tables below link into the text
  Array.prototype.forEach.call(document.querySelectorAll('#best tbody tr, details tbody tr'), function (tr) {
    var td = tr.querySelector('td.num');
    if (!td || !entryById[td.textContent.trim()]) return;
    var id = td.textContent.trim();
    td.innerHTML = '<a href="#entry-' + id + '" title="Show entry ' + id + ' in the text">' + id + '</a>';
  });

  function fromHash() {
    var h = decodeURIComponent(location.hash.slice(1));
    var m;
    if ((m = /^entry-(\w+)$/.exec(h)) && entryById[m[1]]) {
      showEntry(m[1]);
      document.getElementById('text').scrollIntoView();
      scrollToRow(entryById[m[1]].start);
      return true;
    }
    if ((m = /^col-([IVX]+)$/.exec(h)) && ROMAN.indexOf(m[1]) >= 0) {
      showColumn(ROMAN.indexOf(m[1]), { keepHash: true });
      return true;
    }
    if ((m = /^L-([IVX]+)-(\d+)$/.exec(h)) && lineCol[m[1] + ' ' + m[2]] != null) {
      goTo(m[1] + ' ' + m[2]);
      showLine(m[1] + ' ' + m[2]);
      var row = document.getElementById(h);
      if (row) row.scrollIntoView({ block: 'center' });
      return true;
    }
    return false;
  }
  window.addEventListener('hashchange', fromHash);

  buildStrip();
  panel.innerHTML = helpHtml();
  if (!fromHash()) showColumn(0, { keepHash: true });
})();
