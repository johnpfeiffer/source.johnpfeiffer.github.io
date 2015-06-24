Title: Test Driven Development Introduction and QA Domains
Date: 2012-01-20 17:44
Tags: tests, tdd, qa, edge cases

[TOC]

### Why Test Driven Development 

"6% progress" in engineering

- Cost: Organizations want to reduce the time and cost associated with releasing code including the post release support, debugging, and maintenance.

- Agility: TDD enables faster product reactions to market changes and more drastic product changes and continued extension of successful products

- Growth: it’s a proven method for Organizations building a strong brand and looking for 6% compound growth, enables larger teams and rotation of personnel

- Individual Time: less time is spent in long debugging session or writing "dead code" (code that never reaches production for either Business reasons – i.e. no customer demand, or Engineering decisions – i.e. quality of the overall product never reaches a release point).

- Individual Careers: ability to work on more complex projects and clear contribution to business success

- Individual Satisfaction: confidence in what’s been delivered and happier users


### Acceptance Test Driven Development			

**Everyone agrees on done!**

	Automated Tests create concrete artifacts for all stakeholders (i.e. PM, QA, Engineering, etc.) to understand scope, review progress, and agree on "done".   This vastly improves inefficiencies in communication, scheduling, and manual testing.
	Design is codified into a common language of Tests:
- Specifications require less translation and have faster validation
- Deliverables are more accurate to the business needs and progress is more accurate
- Future maintenance and extendibility is built into the process

Acceptance Tests do require more up front discussions (not coding!) and setup time for automation.  
Good tests must match production environments and requirements in order to be valid.  

Tests must be engineered well in order to give good results as they are a product too.
TDD does not guarantee good designs, good thinking, or good code.  It’s up to people to make it work.

(Unit) Test Driven Development		Simple, easy, lean, fast, readable, and early.

- Testing should be easy so start small, ask questions, and get used to the world being upside down =)
- Tests must factor out Dependencies (helps design modularization and isolation)
- Tests must run fast (slow tests can be moved into Acceptance Testing)
- Consider writing tests in order of expected probability of occurrence (balanced by severity if coverage is missed) i.e. the most common usage is correct inputs generating correct output, next maybe 2% of invalid inputs will generate 85% of data corruption

- -"Happy Path" verifies that the code will fulfill the functionality specifically asked for so these are the "high value" tests.
- - Next verify most likely invalid inputs and important exception handling
- The law of diminishing returns: more tests means more code writing and more tests that require maintenance
- Tests uncover assumptions, dependencies, tight coupling, and duplication.
- Every Developer must be able to read and maintain the tests; it is a shared effort at making a better product so clarity and readability are critical.


### TDD Workflow

            
    Write Acceptance Test -> Run Acceptance Test -> Passes = Next TDD feature please =)
                             /                 ^
                 AT Fails   /                  | UT Passes
                           /                   |
                      Write Unit Test -> Run Unit Tests
                                          \    ^
                                 UT Fails  \   |
                                            \  |
                                      Write Code to make it pass

							
#### Trivial Example using an "Adding Positive Integers Only Calculator" 	 

add( int a , int b)
- testPositiveIntegerPlusPositiveInteger ("happy path")
- testIntegerMinusPositiveInteger (invalid input)
- testZeroPlusPositiveInteger (invalid input)
- testStringPlusInteger (edge case invalid input: maybe the compiler does not catch this)

#### "Test Doubles" using Stubs or Mocks (Factoring out dependencies)
Using stubs or mocks we can focus testing only the code we’ve written, Stubs generally are simple hard coded ways to validate state.

### Source code examples of TDD

    add(int a, int b) {
        dependencyLibrary.adder(a, b)
    }

    Class dependencyLibraryStub extends dependencyLibrary {
        	dependencyLibraryStub(expectedResult)
        Override adder(int a, int b)
        {
            	return expectedResult
        }
    }

Mocks are usually leveraged with a framework and can validate process, multiple interactions, as well as state.


### QA Domains

- Start Testing with the most used paths and most user visible areas.
- Find the most serious consequence -> force error handling or crash.
- Make it easy to test (invest in GUI / scripting, don't slow testing down by requiring careful command line typing)
- Automate testing (especially regression testing).

    :::text
    functionality
    communication / documentation
    command structure
    performance / load
    output (including error messages)
    compatible softare / hardware
    stack overflow
    garbage collection
    
    errors - boundary
            -math / time
            -startup
            -long running
            -pause & restart / resume
            -backup & restore
            -different data back & forth
            -race conditions
            -denial of resources
    

#### Dependencies

    :::text
    RAM full, Hard Drive full scenarios, cpu full, network slow
    locked files (e.g. OS is using)
    Error accessing media (slow disk, bad network, etc.)
    Other Shared Resource locks?
    Special Modes (i.e. airplane/offline mode, disconnected peripheral, etc.
    
    Remove/Rename files and folders the app depends on
      Corrupt one of the above
      hidden file? permissions changed...
    
#### File Systems, Language, and Text

- Ascii vs UTF8
- File size 0, negative? and very large
- Many small files, many large files
- Directory or Folder instead of File and vice versa
- Symbolic links and shortcuts

- Invalid paths (OS do the checks!)
- Max path length
- longest file name (symbols)
- reserved file names?


- try pasting (rather than typing)
- special control chars \n  <a href  
    `-1234567890-1234567890--1234567890--1234567890`


- Escape sequences

    :::text
    ‘\’. ‘\’ = %5C = %255C = %%35%63 = %25%35%63 )
    
HTML Encoding check where applicable: ‘<’ = < = &#x3C = &60

!  #   $  

##### byte boundaries

    0 to 65,535
    -2,147,483,648 to 2,147,483,647



#### Standard Test Cases 

#### Viewing

 Resolution 1024 x 768 but also try 800x600 and 1280 and strange ones
 Resizing?
 Excessive Requests
 performance (too slow might be unusable)
  
 Single item too long horizontal
 Single item too long vertical
 Too many items returned horizontal 
 Too many items returned vertical


- Dropdown 
 scrollbar = logical / physical batches of results?

- Web Page
 chrome, firefox(2,3), ie (6,7,8,9), safari (i.e. without SSO), opera?
 able to bookmark 


#### User Input

Text Entry
 too few (blank) and too many chars
 funny chars (UTF8? and symbols !@#$%&^*()[]\|;':",./<>?
 Special case = Email Address or Phone Number?
 Excessive Submits

Login 
 wrong username
 wrong password
 already logged in
 username does not exist?
 user does not have permission?
 back button

Search (similar to above but also includes)

  case sensitive? (user notified?)
  wild card
  no data set exists to search (e.g. user search but no users?)


#### Upload a file
1. UTF8 file names, very long names, very short names, special characters (. / ? < >)
2. case sensitivity, reserved key names
3. upload normal expected extensions (jpg, gif, png etc.)
4. try random or restricted extensions (.exe, .bat, no extension, super long chars, special chars)
5. tiny file or really large file
6. 0 byte file
7. compressed (zip, 7z, rar, etc.)
8. interrupt the upload (does it fail cleanly? resume?)
9. race condition of two different sessions uploading the same file name (different content)


#### Whitebox "Glassbox" Looking in the code

- InvalidSession Exception
- Offline Exception, 
- No Permission Exception
- Could not retrieve from source Exception
- Unexpected Exception

- array boundary
- memory leaks / free
- race conditions / locked
- global variables (creates a hidden race condition or lock)


#### Error Messages

- Do they appear when there's a problem?
- Are they accurate?
- Can they be understood?
- Do they direct the user on how to the correct the problem?

**What to log or print in an error**

    Title = source of the error 
    You cannot do "action user tried".
    Reason why Source is throwing error.

    "MyComponent Driver Error"
    You cannot reply to "user@domain.com"
    You do not have write permission on that file.


### For your consideration

#### Stress
- "thundering herd" and exponential backoff
- cpu processing, data sizes, input volumes, frequency
- what breaks when it fails
- can it be disabled

#### Time
- concurrency
- stale/null/indeterminate state
- archived/deleted

#### Operations
- upgrades, migrations, backups/restore
- UX: new users and new features
- power users vs newbs vs admins, international, 3rd party devs, support
- logging, metrics, and analytics

#### Platform
- variability in OS, browser, screens, devices, databases, connections
- external dependency handling?
- licensing and tier thresholds (i.e. group storage limit)
- SaaS vs cluster vs on premise considerations

#### Usability
- consistency
- empty state, keyboard vs mouse vs ?
- customization? (saved preferences)
- what's the learning curve? too little/too much documentation?
- list UI: sorting, ordering, 

#### Security
- Access and Audit logs
- who should be able to access via Web UI, API, etc.
- XSS, XSRF
- where's the edge? tiered service layers (clearly defined boundaries for authorization)
- leaking information (what can anonymous or normal users see they should not)
- logging password/sensitive info
