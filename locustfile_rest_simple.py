"""
Simplified Locust load testing for REST API (Read-only)
Tests only GET endpoints

Endpoints tested:
- GET /terms - List all terms
- GET /terms/{id} - Get specific term
- GET /graph - Get full semantic graph

Usage:
    locust -f locustfile_rest_simple.py --host=http://localhost:8000 \
        --users 50 --spawn-rate 5 --run-time 3m --headless
"""

from locust import HttpUser, task, between
import random
import os


class RESTUser(HttpUser):
    """
    Read-only user for REST API testing
    Realistic browsing behavior with different endpoint weights
    """
    wait_time = between(1, 3)
    
    def on_start(self):
        """Initialize user session data"""
        self.existing_terms = []
        response = self.client.get("/terms", name="GET /terms [init]")
        if response.status_code == 200:
            try:
                data = response.json()
                if isinstance(data, list):
                    self.existing_terms = [term.get('term', term.get('id')) for term in data if term.get('term') or term.get('id')]
            except:
                pass
    
    @task(35)
    def view_all_terms(self):
        """GET /terms - Most frequent operation (view all terms)"""
        with self.client.get("/terms", catch_response=True, name="GET /terms [LIGHT]") as response:
            if response.status_code == 200:
                try:
                    data = response.json()
                    if isinstance(data, list):
                        self.existing_terms = [term.get('term', term.get('id')) for term in data if term.get('term') or term.get('id')]
                    response.success()
                except Exception as e:
                    response.failure(f"Failed to parse response: {e}")
            else:
                response.failure(f"Got status code {response.status_code}")
    
    @task(28)
    def view_graph(self):
        """GET /graph - Very heavyweight: full semantic graph"""
        with self.client.get("/graph", catch_response=True, name="GET /graph [HEAVY]") as response:
            if response.status_code == 200:
                try:
                    data = response.json()
                    if 'nodes' in data and 'edges' in data:
                        response.success()
                    else:
                        response.failure("Invalid graph structure")
                except Exception as e:
                    response.failure(f"Parse error: {e}")
            else:
                response.failure(f"Got status code {response.status_code}")
    
    @task(17)
    def view_specific_term(self):
        """GET /terms/{term} - Lightweight: fast single term lookup"""
        if not self.existing_terms:
            term_id = random.choice(['FastAPI', 'Python', 'Docker', 'SQLite', 'REST API', 'ORM'])
        else:
            term_id = random.choice(self.existing_terms)
        
        with self.client.get(
            f"/terms/{term_id}",
            catch_response=True,
            name="GET /terms/{term} [LIGHT]"
        ) as response:
            if response.status_code == 200:
                response.success()
            elif response.status_code == 404:
                
                response.success()
            else:
                response.failure(f"Unexpected status {response.status_code}")
    
    @task(10)
    def browse_multiple_terms(self):
        """Browse multiple specific terms in sequence"""
        if len(self.existing_terms) >= 3:
            selected_terms = random.sample(self.existing_terms, 3)
            for term_id in selected_terms:
                self.client.get(f"/terms/{term_id}", name="GET /terms/{term} [browse]")
    
    @task(10)
    def view_terms_then_graph(self):
        """Realistic pattern: view terms, then view graph"""
        self.client.get("/terms", name="GET /terms [pattern]")
        self.client.get("/graph", name="GET /graph [pattern]")


class LightUser(HttpUser):
    """
    Light user - only views terms list and specific terms
    No heavy graph operations
    """
    wait_time = between(0.5, 2)
    
    def on_start(self):
        """Initialize user session data"""
        self.existing_terms = []
        response = self.client.get("/terms")
        if response.status_code == 200:
            try:
                data = response.json()
                if isinstance(data, list):
                    self.existing_terms = [term.get('term', term.get('id')) for term in data if term.get('term') or term.get('id')]
            except:
                pass
    
    @task(60)
    def view_terms(self):
        """GET /terms"""
        self.client.get("/terms", name="GET /terms [light]")
    
    @task(40)
    def view_specific(self):
        """GET /terms/{term}"""
        if self.existing_terms:
            term_id = random.choice(self.existing_terms)
            self.client.get(f"/terms/{term_id}", name="GET /terms/{term} [light]")


class HeavyUser(HttpUser):
    """
    Heavy user - frequently requests the graph
    Tests system under computationally intensive workload
    """
    wait_time = between(2, 5)
    
    @task(50)
    def view_graph_repeatedly(self):
        """Request graph multiple times (very intensive)"""
        self.client.get("/graph", name="GET /graph [heavy]")
    
    @task(30)
    def view_all_terms(self):
        """Get all terms"""
        self.client.get("/terms", name="GET /terms [heavy]")
    
    @task(20)
    def view_terms_and_graph(self):
        """View terms and graph together"""
        self.client.get("/terms", name="GET /terms [heavy-pattern]")
        self.client.get("/graph", name="GET /graph [heavy-pattern]")


class StressUser(HttpUser):
    """
    Stress testing user with minimal wait time
    Used for stress tests to find breaking points
    """
    wait_time = between(0.1, 0.5)
    
    @task(50)
    def rapid_reads(self):
        """Rapid term list requests"""
        self.client.get("/terms", name="GET /terms [stress]")
    
    @task(30)
    def rapid_graph(self):
        """Rapid graph requests"""
        self.client.get("/graph", name="GET /graph [stress]")
    
    @task(20)
    def rapid_specific(self):
        """Rapid specific term requests"""
        term_id = random.choice(['FastAPI', 'Python', 'Docker', 'SQLite', 'REST API', 'ORM'])
        self.client.get(f"/terms/{term_id}", name="GET /terms/{term} [stress]")


