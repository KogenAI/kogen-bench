# frozen_string_literal: true

# Sandboxed grading has no outbound network. Selenium::WebDriver::Platform.ip finds the local address by "connecting" a UDP socket to
# 8.8.8.8:53 (no packet is sent, it only selects a route), which the sandbox refuses (EPERM). Route that probe to loopback instead.
require "socket"
UDPSocket.prepend(Module.new { def connect(host, port) = super(host == "8.8.8.8" ? "127.0.0.1" : host, port) })
