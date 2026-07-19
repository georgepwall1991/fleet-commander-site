#!/usr/bin/env ruby

require "base64"
require "open3"

APP_STORE_URL = "https://apps.apple.com/gb/app/fleet-commander/id6760207805?uo=4"
REQUIRED_PAGES = [
  "updates/index.html",
  "updates/frontier-fleet-gameplay-spotlight/index.html",
  "updates/opening-arc-and-command-center/index.html"
].freeze

def read_remote(repository, ref, path)
  stdout, status = Open3.capture2(
    "gh", "api",
    "repos/#{repository}/contents/#{path}?ref=#{ref}",
    "--jq", ".content"
  )
  raise "missing #{path}" unless status.success?

  Base64.decode64(stdout)
end

def read_local(root, path)
  full_path = File.join(root, path)
  raise "missing #{path}" unless File.file?(full_path)

  File.read(full_path)
end

arguments = ARGV.each_slice(2).to_h
root = arguments["--root"]
repository = arguments["--repo"]
ref = arguments["--ref"]

reader = if root
           ->(path) { read_local(root, path) }
         elsif repository && ref
           ->(path) { read_remote(repository, ref, path) }
         else
           abort "usage: check-fleet-commander-funnel.rb --root PATH or --repo OWNER/NAME --ref REF"
         end

failures = []
index = reader.call("index.html")
failures << "homepage is missing the App Store CTA" unless index.include?(APP_STORE_URL)
failures << "homepage uses a custom imitation App Store badge" if index.include?('class="app-store-badge"')
unless index.include?("Download Fleet Commander on the App Store")
  failures << "homepage App Store CTA lacks explicit accessible text"
end
failures << "homepage is missing the Updates link" unless index.include?('href="./updates/"')
unless index.include?("Free to download, with no ads and no pay-to-win")
  failures << "homepage drops the preserved GemGame store-model claim"
end

REQUIRED_PAGES.each do |path|
  begin
    reader.call(path)
  rescue RuntimeError
    failures << "missing #{path}"
  end
end

sitemap = reader.call("sitemap.xml")
REQUIRED_PAGES.each do |path|
  route = path.delete_suffix("index.html")
  failures << "sitemap is missing /#{route}" unless sitemap.include?("fleet-commander-site/#{route}")
end

unless failures.empty?
  warn failures.map { |failure| "FAIL: #{failure}" }.join("\n")
  exit 1
end

puts "Fleet Commander public funnel check passed"
