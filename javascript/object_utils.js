/**
 * Object utility snippets for common object operations.
 */

/**
 * Deep clone a plain object / array using JSON serialization.
 * NOTE: Does not support functions, Dates, RegExp, or undefined values.
 * @example deepClone({ a: { b: 1 } }) // { a: { b: 1 } } (new reference)
 */
function deepClone(obj) {
  return JSON.parse(JSON.stringify(obj));
}

/**
 * Deep merge two objects. Properties from source override target for scalars;
 * nested objects are merged recursively.
 * @example deepMerge({ a: 1, b: { x: 1 } }, { b: { y: 2 }, c: 3 })
 *          // { a: 1, b: { x: 1, y: 2 }, c: 3 }
 */
function deepMerge(target, source) {
  const output = { ...target };
  for (const [key, value] of Object.entries(source)) {
    if (value && typeof value === "object" && !Array.isArray(value) &&
        target[key] && typeof target[key] === "object") {
      output[key] = deepMerge(target[key], value);
    } else {
      output[key] = value;
    }
  }
  return output;
}

/**
 * Return a new object containing only the specified keys.
 * @example pick({ a: 1, b: 2, c: 3 }, ['a', 'c']) // { a: 1, c: 3 }
 */
function pick(obj, keys) {
  return Object.fromEntries(keys.filter((k) => k in obj).map((k) => [k, obj[k]]));
}

/**
 * Return a new object with the specified keys removed.
 * @example omit({ a: 1, b: 2, c: 3 }, ['b']) // { a: 1, c: 3 }
 */
function omit(obj, keys) {
  const excluded = new Set(keys);
  return Object.fromEntries(Object.entries(obj).filter(([k]) => !excluded.has(k)));
}

/**
 * Flatten a nested object into a single-level object using dot-notation keys.
 * @example flattenObject({ a: { b: { c: 1 } } }) // { 'a.b.c': 1 }
 */
function flattenObject(obj, prefix = "") {
  return Object.entries(obj).reduce((acc, [key, value]) => {
    const fullKey = prefix ? `${prefix}.${key}` : key;
    if (value && typeof value === "object" && !Array.isArray(value)) {
      Object.assign(acc, flattenObject(value, fullKey));
    } else {
      acc[fullKey] = value;
    }
    return acc;
  }, {});
}

/**
 * Convert an array of objects into a Map keyed by a given property.
 * @example indexBy([{ id: 1, name: 'Alice' }, { id: 2, name: 'Bob' }], 'id')
 *          // Map { 1 => { id: 1, name: 'Alice' }, 2 => { id: 2, name: 'Bob' } }
 */
function indexBy(array, key) {
  return new Map(array.map((item) => [item[key], item]));
}

/**
 * Check if two plain objects are deeply equal.
 * @example deepEqual({ a: [1, 2] }, { a: [1, 2] }) // true
 */
function deepEqual(a, b) {
  if (a === b) return true;
  if (typeof a !== "object" || typeof b !== "object" || a === null || b === null)
    return false;
  const keysA = Object.keys(a);
  const keysB = Object.keys(b);
  if (keysA.length !== keysB.length) return false;
  return keysA.every((k) => deepEqual(a[k], b[k]));
}

module.exports = { deepClone, deepMerge, pick, omit, flattenObject, indexBy, deepEqual };
