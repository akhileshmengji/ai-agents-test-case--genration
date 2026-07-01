# Acme LMS Product Knowledge

Purpose: Permanent product knowledge for Acme LMS (a fictional online course
platform used only as a worked example for this toolkit). This is the file
the AI agent reads before analysing any user story in `examples/acme-lms/stories/`.

## 1. Product Overview
- Product Name: Acme LMS
- Acme LMS is an online course platform: instructors create courses, invite
  students, and track progress; students enroll in courses and complete
  lessons.
- Platforms: Web, Android, iOS

## 2. User Roles
- Instructor
- Student
- Admin

## 3. Core Modules
Auth, Dashboard, Course, Invite, Lesson Player, Progress Reports,
Notifications, Profile

## 4. Role Capabilities
- Instructor: create/edit/delete courses, invite students, view progress
  reports, send notifications. Instructor CANNOT modify a student's
  submitted quiz answers.
- Student: enroll in courses, accept invitations, complete lessons, view
  own progress. Student CANNOT invite other students or edit course content.

## 5. Authentication & Session Rules
- Login method: Email + password, or Email + OTP for invite-flow signup.
- OTP expires after 10 minutes.
- Resend OTP available after 60 seconds.
- Only the latest OTP is valid.
- Session remains active for 30 days on mobile, until browser close on web.

## 6. Invitation Rules (Course Enrollment)
- Instructor invites a student to a course via email.
- Invite link is valid for 14 days; becomes invalid immediately after
  successful enrollment (single-use).
- If the invited student is already enrolled in the course, the invite
  resolves to an "already enrolled" state rather than creating a duplicate
  enrollment.
- An instructor may re-invite the same email to the same course after the
  original invite expires unused.

## 7. Non-Functional Baselines
- Performance SLA: invite screen loads P95 <= 2000ms on 4G; enroll API
  responds P95 <= 2000ms.
- Accessibility standard: WCAG 2.1 AA across web and mobile.
- Supported browsers: latest Chrome, Edge, Safari (macOS + iOS).
