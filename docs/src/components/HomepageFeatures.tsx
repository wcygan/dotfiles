import React from "react";
import clsx from "clsx";
import styles from "./HomepageFeatures.module.css";

type FeatureItem = {
  title: string;
  description: JSX.Element;
};

const FeatureList: FeatureItem[] = [
  {
    title: "Safe Installation",
    description: (
      <>
        Automatic backups before any changes. Easy rollback if something goes
        wrong. Your existing configuration is always protected.
      </>
    ),
  },
  {
    title: "Modern Developer Tools",
    description: (
      <>
        Pre-configured for modern CLI tools like ripgrep, fd, bat, and eza.
        Built with Deno TypeScript for cross-platform compatibility.
      </>
    ),
  },
  {
    title: "Customizable Configuration",
    description: (
      <>
        Organized shell configuration with separate files for aliases, functions,
        and exports. Easy to extend and personalize for your workflow.
      </>
    ),
  },
];

function Feature({ title, description }: FeatureItem) {
  return (
    <div className={clsx("col col--4")}>
      <div className="text--center padding-horiz--md">
        <h3>{title}</h3>
        <p>{description}</p>
      </div>
    </div>
  );
}

export default function HomepageFeatures(): JSX.Element {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => <Feature key={idx} {...props} />)}
        </div>
      </div>
    </section>
  );
}
