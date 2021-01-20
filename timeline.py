import spacy
import pandas as pnd
import numpy as np
import matplotlib.pyplot as plt

nlp = spacy.load('en_core_web_lg')
essay = 'sample essay goes here'
doc = nlp(essay)

#timeline of the essay by examining verbs
if(essay):
    verbPast = []
    verbPres = []
    verbListNew = []
    previdx = 0
    for word in doc:
        if (word.pos_ == 'VERB'):
            verbRawList.append(word)
        if (word.pos_ != 'VERB'):
            verbRawList.append('0')
    for n in range(len(verbRawList)):
        if (n == 0 and str(verbRawList[n]) != '0'):
            verbListNew.append(verbRawList[n])
            previdx = n
        elif (n != 0 and str(verbRawList[n]) != '0'):
            if (n - previdx == 1):
                verbListNew[-1] += ' ' + verbRawList[n]
            verbListNew.append(verbRawList[n])
    tok = 0
    for i in range(len(verbListNew)):
        v = nlp(str(verbListNew[i]))
        lll = len(verbListNew[i])
        if (lll == 1):
            if (nlp.vocab.morphology.tag_map[v[0].tag_]['Tense_past']):
                verbPast.append(v)
            if (nlp.vocab.morphology.tag_map[v[0].tag_]['Tense_pres']):
                verbPres.append(v)
        if (lll == 2):
            if (nlp.vocab.morphology.tag_map[v[0].tag_]['VerbType_mod'] and nlp.vocab.morphology.tag_map[v[1].tag_]['Tense_pres'] and nlp.vocab.morphology.tag_map[v[1].tag_]['Aspect_prog']):
                verbPres.append(v)
            if (nlp.vocab.morphology.tag_map[v[0].tag_]['VerbType_mod'] and nlp.vocab.morphology.tag_map[v[1].tag_]['VerbForm_inf']):
                verbPres.append(v)
            if (nlp.vocab.morphology.tag_map[v[0].tag_]['VerbType_mod'] and nlp.vocab.morphology.tag_map[v[1].tag_]['VerbForm_part']):
                verbPast.append(v)
                for u in v:
                    if (u not in ['have', 'has', 'had']):
                        notOrderedWell += 1
        if (lll == 3):
            if (nlp.vocab.morphology.tag_map[v[0].tag_]['VerbType_mod'] and nlp.vocab.morphology.tag_map[v[1].tag_]['VerbForm_part'] and nlp.vocab.morphology.tag_map[v[2].tag_]['Tense_pres'] and nlp.vocab.morphology.tag_map[v[2].tag_]['Aspect_prog']):
                verbPast.append(v)
    verbTimeline = {}
    for past in verbPast:
        for o in verbListNew:
            if (past == o):
                verbTimeline[past] = verbListNew.index(o)
    verbTimeline['present'] = 'present'
    for pres in verbPres:
        for q in verbListNew:
            if (past == q):
                verbTimeline[pres] = verbListNew.index(q)
    dates = []
    for i in verbTimeline.keys():
        if (i == 'present'):
            dates.append('present')
        dates.append('event')
    #ploting here:
    # Choose some nice levels
    levels = np.tile([-5, 5, -3, 3, -1, 1], int(np.ceil(len(dates)/6)))[:len(dates)]
    # Create figure and plot a stem plot with the date
    fig, ax = plt.subplots(figsize=(8.8, 4), constrained_layout=True)
    ax.set(title="Timeline of verbs in this essay")
    markerline, stemline, baseline = ax.stem(dates, levels, linefmt="C3-", basefmt="k-", use_line_collection=True)
    plt.setp(markerline, mec="k", mfc="w", zorder=3)
    # Shift the markers to the baseline by replacing the y-data by zeros.
    markerline.set_ydata(np.zeros(len(dates)))
    # annotate lines
    vert = np.array(['top', 'bottom'])[(levels > 0).astype(int)]
    for d, l, r, va in zip(dates, levels, verbTimeline, vert):
        ax.annotate(r, xy=(d, l), xytext=(-3, np.sign(l)*3), textcoords="offset points", va=va, ha="right")
    plt.setp(ax.get_xticklabels(), rotation=30, ha="right")
    # remove y axis and spines
    ax.get_yaxis().set_visible(False)
    for spine in ["left", "top", "right"]:
        ax.spines[spine].set_visible(False)
    ax.margins(y=0.1)
    plt.savefig("timeline.png", dpi=150)
