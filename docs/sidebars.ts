import type { SidebarsConfig } from "@docusaurus/plugin-content-docs";

const sidebars: SidebarsConfig = {
  tutorialSidebar: [
    {
      type: "category",
      label: "Getting Started",
      collapsed: false,
      items: [
        "getting-started/installation",
        "getting-started/quick-start",
      ],
    },
    {
      type: "category",
      label: "Configuration",
      collapsed: false,
      items: [
        "configuration/shell",
        "configuration/editors",
        "configuration/tools",
      ],
    },
    {
      type: "category",
      label: "Reference",
      collapsed: false,
      items: [
        "reference/scripts",
      ],
    },
  ],
};

export default sidebars;
