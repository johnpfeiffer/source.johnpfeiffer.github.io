Title: Server Operations: Cloud versus Build Your Own
Date: 2012-11-08 17:06
Author: John Pfeiffer
Slug: server-operations-cloud-versus-build-your-own

<div class="field field-name-body field-type-text-with-summary field-label-hidden">
<div class="field-items">
<div class="field-item even">
Here's my response to Jeff Atwood's calculations and incorrect
conclusion about Building Your Own Server: I'm not sure I know when an
organization's Production deployment doesn't need reduced
complexity/costs (people!), flexibility for load, and redundancy...

</p>

"Anyway, I want to make it clear that building and colocating your own
servers isn't (always) crazy, it isn't scary, heck, it isn't even
particularly hard. In some situations it can make sense to build and
rack your own servers, provided …

</p>

-you want absolute top of the line server performance without paying
thousands of dollars per month for the privilege  

-you are willing to invest the time in building, racking, and
configuring your servers  

-you have the capital to invest up front  

-you desire total control over the hardware  

-you aren't worried about the flexibility of quickly provisioning new
servers to handle unanticipated load  

-you don't need the redundancy, geographical backup, and flexibility
that comes with cloud virtualization"

</p>

[http://www.codinghorror.com/blog/2012/10/building-servers-for-fun-and-pr...][]

</p>

Hi Jeff, long time fan, first time commenter... I love building servers
too and I've managed a small group of servers, I personally use Linode,
and my currently company uses AWS and some internal servers...

</p>

You would agree that in coding you pick the right tool for the job
(scientific computing would use a different technology stack than
standard ecommerce startup website)...

</p>

\1. AWS is elastic (you pay a premium for being to scale up or down -
and there's value to the agility with which you can change or add new
services)

</p>

\2. AWS RDS is a huge improvement over managing MySQL replication, and
they have ELB and lots of other addons that take serious Ops chops to
create and maintain

</p>

\3. Server operations cost is not the raw hardware:

</p>

\a. The biggest cost in Ops is people (same as coding), so leveraging
Amazon saves on how many people you need to pay to manage your server
farm (yes, SysAdmins take holidays and change jobs so cost = N+1 )...
you can outsource half way by colocating but the setting up the
redundancy, monitoring, auto scaling, etc. becomes a physical pain (you
want West Coast and East Coast servers, right).

</p>

\b. The infrastructure of cooling, UPS, network (bandwidth!), backups,
etc. is also a big factor in Operations (does your server room have
building security? backup generator?)

</p>

My point is that for a stealth mode startup or any internal lab testing
buying servers is a no brainer - do it with ESXi or OpenStack and hack
away!

</p>

BUT for Production you'll need some Cloud strategy (AWS competitors:
RedHat OpenShift, RackSpace Cloud, IBM, ATT Compute, Google AppEngine,
etc. means lower prices and improved services)

</p>

As you've already mentioned if you happen to have hanging around a pile
of cash and tech expertise that's underutilized...

</p>
<p>
</div>
</div>
</div>
<div class="field field-name-taxonomy-vocabulary-1 field-type-taxonomy-term-reference field-label-above clearfix">
### tags:

-   [IT][]

</div>
</p>

  [http://www.codinghorror.com/blog/2012/10/building-servers-for-fun-and-pr...]:
    http://www.codinghorror.com/blog/2012/10/building-servers-for-fun-and-prof-ok-maybe-just-for-fun.html
  [IT]: http://john-pfeiffer.com/category/it
