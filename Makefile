# Example Makefile to edit

SHELL := /bin/bash

.PHONY: help \
        stage \
        status \
        changes \
        env-dev \
        stage_out


.DEFAULT_GOAL := help


# --------------------------------------------------
# Help
# --------------------------------------------------

help:
	@echo ""
	@echo "Repository Commands"
	@echo "=================="
	@echo ""
	@echo "Git:"
	@echo "  make stage       Stage changed files"
	@echo "  make status      Show repository status"
	@echo "  make changes     Show staged changes"
	@echo ""
	@echo "Environment:"
	@echo "  make env-dev     Show development environment activation command"
	@echo ""
	@echo "Data:"
	@echo "  make stage_out   Sync stage_out data"
	@echo ""


# --------------------------------------------------
# Git workflow
# --------------------------------------------------

stage:
	./scripts/git/stage_files.sh


status:
	git status --short


changes:
	git diff --cached --name-status


# --------------------------------------------------
# Development environment
# --------------------------------------------------

# Make cannot modify the current interactive shell.
# This prints the correct command to run.
env-dev:
	@echo ""
	@echo "Activate development environment with:"
	@echo ""
	@echo "source scripts/dev/env-dev.sh"
	@echo ""


# --------------------------------------------------
# Data synchronisation
# --------------------------------------------------

stage_out:
	source scripts/cli/datasync/activate_datasync.sh && \
	datasync sync stage_out
