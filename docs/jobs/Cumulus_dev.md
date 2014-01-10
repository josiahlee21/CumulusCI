# Job: Cumulus_dev

## Overview

The Cumulus_dev job runs after each commit to the repository and at scheduled times to ensure the dev branch passes all Apex tests.

## Target Org

This job uses a dedicated target org, cumulus.dev, to 

## Configuration

### Title and Description

![Cumulus_dev - Title and Description](https://raw.github.com/SalesforceFoundation/CumulusCI/master/docs/jobs/cumulus_dev-title.png)

### Source Code Management

![Cumulus_dev - SCM](https://raw.github.com/SalesforceFoundation/CumulusCI/master/docs/jobs/cumulus_dev-scm.png)

### Triggers

![Cumulus_dev - Triggers](https://raw.github.com/SalesforceFoundation/CumulusCI/master/docs/jobs/cumulus_dev-triggers.png)

### Build

![Cumulus_dev - Build](https://raw.github.com/SalesforceFoundation/CumulusCI/master/docs/jobs/cumulus_dev-build.png)

### Post Build

If the build passes, we kick off a build of [Cumulus_dev_cinnamon_deploy](https://github.com/SalesforceFoundation/CumulusCI/blob/master/docs/jobs/Cumulus_dev_cinnamon_deploy.md)

The Editable Email Notification post build action is used to send a formatted email to the developer who committed the last commit in the push.

The *Set build status on GitHub commit* post build action flags the GitHub commit with the build status so the Branches list and Pull Requests for the branch show the build status with a link to the build job for more details.

![Cumulus_dev - Post Build](https://raw.github.com/SalesforceFoundation/CumulusCI/master/docs/jobs/cumulus_dev-post_build.png)