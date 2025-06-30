// eslint.config.js
import js from "@eslint/js";
import globals from "globals";

export default [
  js.configs.recommended, // Base recommended JS rules

  {
    languageOptions: {
      ecmaVersion: "latest",
      sourceType: "module",
      globals: {
        ...globals.browser,
        ...globals.node,
      },
    },
    rules: {
      // Your custom rules here
      "no-unused-vars": "warn",
      "no-console": "off",
      eqeqeq: "error",
    },
  },
];
