---
title: "Contribute to This Blog"
date: 2020-11-07T12:59:31+01:00
draft: false
summary: in this blog post i ll show you how you can create a PR to edit contents of this blog
---

# Introduction

This blog is a statically rendered blog, by using hugo/netlify and a few other technologies. In a nutshell there is a repo: https://github.com/loeken/blog which contains the markup for reach blogpost ( this blogpost for example can be found [here](https://github.com/loeken/blog/blob/master/content/posts/contribute-to-this-blog.md))

So if you think i fucked up on some article, made a mistake - or you know a better explanation and wish to share it with others feel free to create a pull request on a seperate branch.

How to best understand this? correct - with an example


### Example

So i wanted to do a quick edit to the blog anyways to add a little link to each article, which allows to you to create an issue on the github repo ( for questions etc ). the change looks like this and adds a link to creating a github issue to each blogpost

![Create Issue at Github](/media/img/create_issue.png)

So to get started we go to edit the file in question:
https://github.com/loeken/blog/edit/master/themes/toha/layouts/_default/single.html

We create a commit with the changes we want to make and give it a description

![Create Commit at Github](/media/img/create_commit_on_branch.png)

And then we create a pull request:

![Create PR at Github](/media/img/create_pr.png)

Then on my side it does build a preview of that change so i can view/test/approve it.
![Create PR at Github](/media/img/pr_preview.png)

-After the PR has been merged it will be pushed to production automatically.
+After the Pull Request has been merged it will be pushed to production automatically.
