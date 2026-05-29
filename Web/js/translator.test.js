// Unit tests for the shared UWU translator. Run with:  node --test Web/js
'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const { uwuTranslate, applyDictionary } = require('./translator.js');

const D = { dict: { 'код': 'кодик~', 'wolf': 'wuffie' }, noises: [] };

test('empty input -> empty string', () => {
    assert.equal(uwuTranslate('', D), '');
    assert.equal(uwuTranslate('   ', D), '');
});

test('dictionary replaces whole Cyrillic word (the \\b JS bug fix)', () => {
    assert.equal(uwuTranslate('код', D), 'кодик~');
});

test('dictionary is case-insensitive', () => {
    assert.equal(uwuTranslate('КОД', D), 'кодик~');
    assert.equal(uwuTranslate('WOLF', D), 'wuffie');
});

test('dictionary matches whole words only (no substring match)', () => {
    assert.ok(!uwuTranslate('кодекс', D).includes('кодик~'));
});

test('english phonetics: n + vowel -> ny', () => {
    assert.equal(uwuTranslate('na', { dict: {}, noises: [] }), 'nya');
});

test('russian phonetics: р -> ль', () => {
    const out = uwuTranslate('трава', { dict: {}, noises: [] });
    assert.ok(!out.includes('р'));
    assert.ok(out.includes('ль'));
});

test('no noise when noises is empty', () => {
    assert.equal(uwuTranslate('код.', D), 'кодик~.');
});

test('noise injected deterministically with seeded random', () => {
    const out = uwuTranslate('код.', {
        dict: {}, noises: [' *гав*'], noiseProbability: 1, random: () => 0,
    });
    assert.ok(out.includes(' *гав*'));
});

test('applyDictionary preserves the boundary char', () => {
    assert.equal(applyDictionary('а код б', { 'код': 'X' }), 'а X б');
});
