---
layout: post
title: PhD Status — Completed!
categories: phd thesis
---


My doctorate studies are finally completed!
The work was done, the thesis submitted, viva voce (oral examination) passed, and minor corrections completed, and today is the day of my graduation at Edinburgh.

My PhD thesis is titled *Decoding information from neural populations in the visual cortex*.
If you are interested in seeing what it was all about, you can look through this approachable [lay summary](#lay-summary) of the contents, which gives an overview without using any technical jargon.

Fellow researchers may be interested in reading the [abstract](#abstract), which provides a more technical description and assumes some familiarity with the field of research (neuroinformatics).

If you want to delve into some of the content from the full thing, [here is a copy of the thesis (PDF)][thesis-pdf].
There is also a [printer-friendly copy (PDF)][thesis-print-pdf], which uses black for all the links (which looks better when printed, as well as saving on toner).


[thesis-pdf]: /LoweSC_PhD_thesis.pdf
[thesis-print-pdf]: /LoweSC_PhD_thesis_printfriendly.pdf
[thesis-abstract-pdf]: /LoweSC_PhD_abstract.pdf
[thesis-laysummary-pdf]: /LoweSC_PhD_laysummary.pdf


## Abstract

Visual perception in mammals is made possible by the visual system and the visual cortex.
However, precisely how visual information is coded in the brain and how training can improve this encoding is unclear.

The ability to see and process visual information is not an innate property of the visual cortex.
Instead, it is learnt from exposure to visual stimuli.
We first considered how visual perception is learnt, by studying the perceptual learning of contrast discrimination in macaques.
We investigated how changes in population activity in the visual cortices V1 and V4 correlate with the changes in behavioural response during training on this task.
Our results indicate that changes in the learnt neural and behavioural responses are directed toward optimising the performance on the training task, rather than a general improvement in perception of the presented stimulus type.
We report that the most informative signal about the contrast of the stimulus within V1 and V4 is the transient stimulus-onset response in V1, 50ms after the stimulus presentation begins.
However, this signal does not become more informative with training, suggesting it is an innate and untrainable property of the system, on these timescales at least.
Using a linear decoder to classify the stimulus based on the population activity, we find that information in the V4 population is closely related to the information available to the higher cortical regions involved with decision making, since the performance of the decoder is similar to the performance of the animal throughout training.
These findings suggest that training the subject on this task directs V4 to improve its read out of contrast information contained in V1, and cortical regions responsible for decision making use this to improve the performance with training.
The structure of noise correlations between the recorded neurons changes with training, but this does not appear to cause the increase in behavioural performance.
Furthermore, our results suggest there is feedback of information about the stimulus into the visual cortex after 300ms of stimulus presentation, which may be related to the high-level percept of the stimulus within the brain.
After training on the task, but not before, information about the stimulus persists in the activity of both V1 and V4 at least 400ms after the stimulus is removed.

In the second part, we explore how information is distributed across the anatomical layers of the visual cortex.
Cortical oscillations in the local field potential (LFP) and current source density (CSD) within V1, driven by population-level activity, are known to contain information about visual stimulation.
However the purpose of these oscillations, the sites where they originate, and what properties of the stimulus is encoded within them is still unknown.
By recording the LFP at multiple recording sites along the cortical depth of macaque V1 during presentation of a natural movie stimulus, we investigated the structure of visual information encoded in cortical oscillations.
We found that despite a homogeneous distribution of the power of oscillations across the cortical depth, information was compartmentalised into the oscillations of the 4–16Hz range at the granular (G, layer 4) depths and the 60–170Hz range at the supragranular (SG, layers 1–3) depths, the latter of which is redundant with the population-level firing rate.
These two frequency ranges contain independent information about the stimulus, which we identify as related to two spatiotemporal aspects of the visual stimulus.
Oscillations in the visual cortex with frequencies <40Hz contain information about fast changes in low spatial frequency.
Frequencies >40Hz and multi-unit firing rates contain information about properties of the stimulus related to changes, both slow and fast, at finer-grained spatial scales.
The spatiotemporal domains encoded in each are complementary.
In particular, both the power and phase of oscillations in the 7–20Hz range contain information about scene transitions in the presented movie stimulus.
Such changes in the stimulus are similar to saccades in natural behaviour, and this may be indicative of predictive coding within the cortex.


## Lay Summary

The most complicated system known to man is that of his own brain.
It's often said that the human mind is the most powerful supercomputer on Earth, though this comparison can seem contrived as the two, brains and computers, clearly work in very different ways.
However, brains are, fundamentally, systems which process information about the world experienced through the senses (sight, hearing, touch, taste, smell, and others besides) and do computations so that we can extract meaning from this data — distinguish the smell of a rose, tell the difference between a cat and a dog, recognise the face of a loved one.
As we progress through the regions of the brain, moving from the parts directly connected to the sensory organs (eyes, ears, and so on), to the deeper recesses of the mind, representations within the brain become increasingly abstract.
Eventually the information about the world, now processed by other parts of the brain to pick out the really important bits, reach the regions of the brain involved in planning and decision making.

Since brains are information processing systems, we can study them using the tools of information theory to try to better understand how they function.
In this thesis, we study how the parts of the brain which process visual information work and allow us to see.
When babies are born, their brains don't know how to handle the information from their eyes; they have to learn how to see.
Even as an adult, you can train your brain to form better representations of the things that you see.
If you repeatedly look at similar images and try to distinguish between them, you will get better with practice (though not forever — at some point your performance will stop improving).
However, we don't know exactly what changes in the brain to enable you to do this.

We investigated this by tasking monkeys to distinguish between similar stimuli — one image but presented with many different contrasts — and recording the activity in their brains as they learnt to get better at this task.
We found that the first part of the brain which processes vision (known as V1) was already very good at encoding the differences between the stimuli.
In fact, it was so good that it didn't need to get better than it was to begin with.
Another part of the brain (known as V4), which analyses more abstract properties of the shapes of visual stimuli, initially didn't distinguish between the contrast of the stimuli.
But it got better with training, and the increase in information in this bit of the brain was the same as the increase in the performance of the monkey.
This suggests that the parts of the monkey's brain which make the decision about how to respond to the stimulus have to use the information in the latter part of the brain (V4) and don't get to use the information which is in the first part (V1).
One hypothesis is that this happens because V1 only has lots of information about these stimuli due to a quirk related to them being different contrasts.
Stimuli in the real world vary in more important ways, and identifying the contrast of what you're seeing doesn't really help you to tell the difference between a bear and tree if you're out in the woods.
Only by training yourself on the task of contrast discrimination does your brain learn to focus on this, presumably less important, feature.

We then turned our attention to the oscillatory activity occurring in the part of the brain which first processes vision (V1).
In the brain, the activity of neurons neighbouring each other within local regions fluctuate together in rhythmic harmony.
Importantly, the activity of the population can oscillate at more than one frequency at once.
To offer up an analogy, the neurons are like the players in an orchestra with violin, cello, and double bass sections.
The instruments play simultaneously and the high frequency oscillations of the violin (the high pitched notes) sit on top of the medium and slower oscillations of the cello and double bass (both lower pitched notes).
Except in the brain, every neuron can play multiple instruments at once.
Since there are lots of neurons, you can only hear one of the notes when the activity of many of the neurons are synchronised for the same note, otherwise its all just random noise.
The amplitude of these oscillations — how loud the different notes are — varies over time, and some of them are created by the neurons in response to the sensory input (i.e. whatever the individual is looking at).

We studied how the amplitudes of the oscillations were triggered by different properties of natural stimuli by showing monkeys a clip from a Hollywood movie and recording the activity in their primary visual cortex (V1).
The outside of your brain, which includes V1, is made up of 6 layers stacked on top of each other, with each layer the thickness of a sheet of card.
We worked out which of the layers and which of the frequencies of oscillations contained information about the movie.
There are two different oscillations which encode information about the visual stimulus, and they correspond to different properties of the movie.
In particular, the low frequency oscillations relate to sudden, coarse, changes in the movie, which occur whenever there is a scene transition or jump cut.
This sort of change in stimulus is also like what happens when your eyes dart from one thing to another, so this signal may reflect how your brain copes with such sudden changes in visual stimulus.
The higher frequency oscillations relate to the finer details in the movie, like the edges of objects moving around.
Although the amplitude of the oscillations is, on average, the same in all the layers, only particular layers have oscillations which relate to the stimulus.
If we return to our orchestra analogy, this is like splitting our bassists into groups and observing that each group plays loudly and quietly some of the time.
All the groups play loudly as often as each other, but only one of the groups plays loudly when the movie they are accompanying moves from one scene to another.
Consequently, you can tell a when scene transition occurs just by listening to that group play together.
We don't know what causes the other groups to play loudly (or quietly), but we do know it isn't systematically related to the movie they're accompanying.
