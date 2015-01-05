Title: Server Operations: Cloud versus Build Your Own
Date: 2012-11-08 17:06
Tags: cloud, startup planning, ops

Here's my response to Jeff Atwood's calculations and incorrect conclusion about Building Your Own Server: I'm not sure I know when an organization's Production deployment doesn't need reduced
complexity/costs (people!), flexibility for load, and redundancy...

"Anyway, I want to make it clear that building and colocating your own servers isn't (always) crazy, it isn't scary, heck, it isn't even particularly hard. In some situations it can make sense to build and rack your own servers, provided ...

- you want absolute top of the line server performance without paying thousands of dollars per month for the privilege
- you are willing to invest the time in building, racking, and configuring your servers
- you have the capital to invest up front
- you desire total control over the hardware
- you aren't worried about the flexibility of quickly provisioning new servers to handle unanticipated load
- you don't need the redundancy, geographical backup, and flexibility that comes with cloud virtualization"

<http://www.codinghorror.com/blog/2012/10/building-servers-for-fun-and-prof-ok-maybe-just-for-fun.html>


Hi Jeff, long time fan, first time commenter... I love building servers too and I've managed a small group of servers, I personally use Linode, and my currently company uses AWS and some internal servers...

You would agree that in coding you pick the right tool for the job (scientific computing would use a different technology stack than a standard ecommerce startup website)...

1. AWS is elastic (you pay a premium for being to scale up or down - and there's value to the agility with which you can change or add new services)

1. AWS RDS is a huge improvement over managing MySQL replication, and they have Elastic Load Balancing and lots of other addons that take serious Ops chops to create and maintain

1. Server operations cost is not the raw hardware:

    1. The biggest cost in Ops is people (same as coding), so leveraging Amazon saves on how many people you need to pay to manage your server farm (yes, SysAdmins take holidays and change jobs so cost = N+1 )... you can outsource half way by colocating but setting up the redundancy, monitoring, auto scaling, etc. becomes a physical pain (you want West Coast and East Coast  servers, right?).

    1. The infrastructure of cooling, UPS, network (bandwidth!), backups, etc. is also a big factor in Operations (does your server room have building security? a backup generator?)

My point is that for a stealth mode startup or any internal lab testing buying servers is a no brainer - do it with ESXi or OpenStack and hack away!

BUT for Production you'll need some Cloud strategy (AWS competitors: RedHat OpenShift, RackSpace Cloud, IBM, ATT Compute, Google AppEngine, etc. means lower prices and improved services)

Unless, as you've already mentioned, "if you happen to have hanging around a pile of cash and tech expertise that's underutilized..."
