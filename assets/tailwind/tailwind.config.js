/**
 * Tailwind configuration for LLL Reptile
 * Imports site-specific tokens and merges with base config
 */

const createTailwindConfig = require('../../tailwind.base.config.js')
const tokens = require('./tokens/conduit.json')

module.exports = createTailwindConfig(tokens)
