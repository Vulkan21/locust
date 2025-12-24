"""
Simplified Locust load testing for gRPC Glossary Service (Read-only)
Tests only read operations

gRPC Methods tested:
- GetTerm - Lightweight (fast single term lookup)
- SearchTerms - Search with filtering
- ListTerms - Get all terms
- GetTermRelations - Get term relationships

Usage:
    locust -f locustfile_grpc_simple.py --host=localhost:50051 \
        --users 50 --spawn-rate 5 --run-time 3m --headless
"""

from locust import User, task, between, events
import grpc
import time
import random
import os
import sys

try:
    import glossary_pb2
    import glossary_pb2_grpc
except ImportError:
    print("=" * 70)
    print("ERROR: gRPC generated files not found!")
    print("=" * 70)
    sys.exit(1)


class GrpcClient:
    """gRPC client wrapper for Locust"""
    
    def __init__(self, host):
        self.host = host
        self.channel = grpc.insecure_channel(host)
        self.stub = glossary_pb2_grpc.GlossaryServiceStub(self.channel)
    
    def __del__(self):
        if hasattr(self, 'channel'):
            self.channel.close()


class GrpcUser(User):
    """
    Read-only gRPC user for load testing
    Realistic browsing behavior with different method weights
    """
    abstract = True
    wait_time = between(1, 3)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client = GrpcClient(self.host)
        self.existing_terms = []
    
    def on_start(self):
        """Initialize user session data"""
        try:
            request = glossary_pb2.ListTermsRequest()
            response = self.client.stub.ListTerms(request)
            self.existing_terms = [term.term for term in response.terms]
        except Exception as e:
            print(f"Failed to get initial terms: {e}")


class RESTLikeGrpcUser(GrpcUser):
    """
    User simulating REST-like behavior patterns
    """
    
    @task(35)
    def list_all_terms(self):
        """ListTerms - Most frequent operation"""
        start_time = time.time()
        try:
            request = glossary_pb2.ListTermsRequest()
            response = self.client.stub.ListTerms(request, timeout=10)
            
            self.existing_terms = [term.term for term in response.terms]
            
            total_time = int((time.time() - start_time) * 1000)
            events.request.fire(
                request_type="grpc",
                name="ListTerms",
                response_time=total_time,
                response_length=len(response.terms),
                exception=None,
                context={}
            )
        except Exception as e:
            total_time = int((time.time() - start_time) * 1000)
            events.request.fire(
                request_type="grpc",
                name="ListTerms",
                response_time=total_time,
                response_length=0,
                exception=e,
                context={}
            )
    
    @task(28)
    def search_terms(self):
        """SearchTerms - Search with query"""
        start_time = time.time()
        try:

            queries = ["gRPC", "Protocol", "HTTP", "API", "RPC", ""]
            query = random.choice(queries)
            
            request = glossary_pb2.SearchTermsRequest(query=query, limit=10)
            response = self.client.stub.SearchTerms(request, timeout=10)
            
            total_time = int((time.time() - start_time) * 1000)
            events.request.fire(
                request_type="grpc",
                name="SearchTerms",
                response_time=total_time,
                response_length=len(response.terms),
                exception=None,
                context={}
            )
        except Exception as e:
            total_time = int((time.time() - start_time) * 1000)
            events.request.fire(
                request_type="grpc",
                name="SearchTerms",
                response_time=total_time,
                response_length=0,
                exception=e,
                context={}
            )
    
    @task(17)
    def get_specific_term(self):
        """GetTerm - Lightweight single term lookup"""
        start_time = time.time()
        try:
            if not self.existing_terms:
                
                term_id = random.choice(['grpc', 'protobuf', 'http2', 'rpc'])
            else:
                term_id = random.choice(self.existing_terms)
            
            request = glossary_pb2.GetTermRequest(term_id=term_id)
            response = self.client.stub.GetTerm(request, timeout=10)
            
            total_time = int((time.time() - start_time) * 1000)
            events.request.fire(
                request_type="grpc",
                name="GetTerm",
                response_time=total_time,
                response_length=1,
                exception=None,
                context={}
            )
        except grpc.RpcError as e:
            total_time = int((time.time() - start_time) * 1000)
            
            if e.code() == grpc.StatusCode.NOT_FOUND:
                events.request.fire(
                    request_type="grpc",
                    name="GetTerm",
                    response_time=total_time,
                    response_length=0,
                    exception=None,
                    context={}
                )
            else:
                events.request.fire(
                    request_type="grpc",
                    name="GetTerm",
                    response_time=total_time,
                    response_length=0,
                    exception=e,
                    context={}
                )
        except Exception as e:
            total_time = int((time.time() - start_time) * 1000)
            events.request.fire(
                request_type="grpc",
                name="GetTerm",
                response_time=total_time,
                response_length=0,
                exception=e,
                context={}
            )
    
    @task(10)
    def get_term_relations(self):
        """GetTermRelations - Get relationships"""
        start_time = time.time()
        try:
            if not self.existing_terms:
                term_id = 'grpc'
            else:
                term_id = random.choice(self.existing_terms)
            
            request = glossary_pb2.GetTermRelationsRequest(term_id=term_id)
            response = self.client.stub.GetTermRelations(request, timeout=10)
            
            total_time = int((time.time() - start_time) * 1000)
            events.request.fire(
                request_type="grpc",
                name="GetTermRelations",
                response_time=total_time,
                response_length=len(response.relations),
                exception=None,
                context={}
            )
        except grpc.RpcError as e:
            total_time = int((time.time() - start_time) * 1000)
            
            if e.code() == grpc.StatusCode.NOT_FOUND:
                events.request.fire(
                    request_type="grpc",
                    name="GetTermRelations",
                    response_time=total_time,
                    response_length=0,
                    exception=None,
                    context={}
                )
            else:
                events.request.fire(
                    request_type="grpc",
                    name="GetTermRelations",
                    response_time=total_time,
                    response_length=0,
                    exception=e,
                    context={}
                )
        except Exception as e:
            total_time = int((time.time() - start_time) * 1000)
            events.request.fire(
                request_type="grpc",
                name="GetTermRelations",
                response_time=total_time,
                response_length=0,
                exception=e,
                context={}
            )
    
    @task(10)
    def list_then_get(self):
        """Realistic pattern: list terms, then get specific one"""
        self.list_all_terms()
        if self.existing_terms:
            self.get_specific_term()


class LightGrpcUser(GrpcUser):
    """
    Light user - only lists and gets specific terms
    No heavy search operations
    """
    wait_time = between(0.5, 2)
    
    @task(60)
    def list_terms(self):
        """ListTerms"""
        start_time = time.time()
        try:
            request = glossary_pb2.ListTermsRequest()
            response = self.client.stub.ListTerms(request, timeout=10)
            self.existing_terms = [term.term for term in response.terms]
            
            total_time = int((time.time() - start_time) * 1000)
            events.request.fire(
                request_type="grpc",
                name="ListTerms [light]",
                response_time=total_time,
                response_length=len(response.terms),
                exception=None,
                context={}
            )
        except Exception as e:
            total_time = int((time.time() - start_time) * 1000)
            events.request.fire(
                request_type="grpc",
                name="ListTerms [light]",
                response_time=total_time,
                response_length=0,
                exception=e,
                context={}
            )
    
    @task(40)
    def get_term(self):
        """GetTerm"""
        start_time = time.time()
        try:
            if self.existing_terms:
                term_id = random.choice(self.existing_terms)
            else:
                term_id = 'grpc'
            
            request = glossary_pb2.GetTermRequest(term_id=term_id)
            response = self.client.stub.GetTerm(request, timeout=10)
            
            total_time = int((time.time() - start_time) * 1000)
            events.request.fire(
                request_type="grpc",
                name="GetTerm [light]",
                response_time=total_time,
                response_length=1,
                exception=None,
                context={}
            )
        except Exception as e:
            total_time = int((time.time() - start_time) * 1000)
            events.request.fire(
                request_type="grpc",
                name="GetTerm [light]",
                response_time=total_time,
                response_length=0,
                exception=e,
                context={}
            )


class HeavyGrpcUser(GrpcUser):
    """
    Heavy user - frequently searches
    """
    wait_time = between(2, 5)
    
    @task(50)
    def search_repeatedly(self):
        """Repeated searches"""
        start_time = time.time()
        try:
            queries = ["gRPC", "Protocol", "HTTP", "API", "RPC"]
            query = random.choice(queries)
            
            request = glossary_pb2.SearchTermsRequest(query=query, limit=20)
            response = self.client.stub.SearchTerms(request, timeout=10)
            
            total_time = int((time.time() - start_time) * 1000)
            events.request.fire(
                request_type="grpc",
                name="SearchTerms [heavy]",
                response_time=total_time,
                response_length=len(response.terms),
                exception=None,
                context={}
            )
        except Exception as e:
            total_time = int((time.time() - start_time) * 1000)
            events.request.fire(
                request_type="grpc",
                name="SearchTerms [heavy]",
                response_time=total_time,
                response_length=0,
                exception=e,
                context={}
            )
    
    @task(30)
    def list_all(self):
        """List all terms"""
        start_time = time.time()
        try:
            request = glossary_pb2.ListTermsRequest()
            response = self.client.stub.ListTerms(request, timeout=10)
            
            total_time = int((time.time() - start_time) * 1000)
            events.request.fire(
                request_type="grpc",
                name="ListTerms [heavy]",
                response_time=total_time,
                response_length=len(response.terms),
                exception=None,
                context={}
            )
        except Exception as e:
            total_time = int((time.time() - start_time) * 1000)
            events.request.fire(
                request_type="grpc",
                name="ListTerms [heavy]",
                response_time=total_time,
                response_length=0,
                exception=e,
                context={}
            )
    
    @task(20)
    def get_with_relations(self):
        """Get term and its relations"""
        
        start_time = time.time()
        try:
            term_id = random.choice(['grpc', 'protobuf', 'http2', 'rpc'])
            
            request = glossary_pb2.GetTermRequest(term_id=term_id)
            self.client.stub.GetTerm(request, timeout=10)
            
           
            rel_request = glossary_pb2.GetTermRelationsRequest(term_id=term_id)
            response = self.client.stub.GetTermRelations(rel_request, timeout=10)
            
            total_time = int((time.time() - start_time) * 1000)
            events.request.fire(
                request_type="grpc",
                name="GetTerm+Relations [heavy]",
                response_time=total_time,
                response_length=len(response.relations),
                exception=None,
                context={}
            )
        except Exception as e:
            total_time = int((time.time() - start_time) * 1000)
            events.request.fire(
                request_type="grpc",
                name="GetTerm+Relations [heavy]",
                response_time=total_time,
                response_length=0,
                exception=e,
                context={}
            )


class StressGrpcUser(GrpcUser):
    """
    Stress testing user with minimal wait time
    """
    wait_time = between(0.1, 0.5)
    
    @task(50)
    def rapid_list(self):
        """Rapid list requests"""
        start_time = time.time()
        try:
            request = glossary_pb2.ListTermsRequest()
            response = self.client.stub.ListTerms(request, timeout=5)
            
            total_time = int((time.time() - start_time) * 1000)
            events.request.fire(
                request_type="grpc",
                name="ListTerms [stress]",
                response_time=total_time,
                response_length=len(response.terms),
                exception=None,
                context={}
            )
        except Exception as e:
            total_time = int((time.time() - start_time) * 1000)
            events.request.fire(
                request_type="grpc",
                name="ListTerms [stress]",
                response_time=total_time,
                response_length=0,
                exception=e,
                context={}
            )
    
    @task(30)
    def rapid_search(self):
        """Rapid search requests"""
        start_time = time.time()
        try:
            query = random.choice(["gRPC", "API", "HTTP"])
            request = glossary_pb2.SearchTermsRequest(query=query, limit=10)
            response = self.client.stub.SearchTerms(request, timeout=5)
            
            total_time = int((time.time() - start_time) * 1000)
            events.request.fire(
                request_type="grpc",
                name="SearchTerms [stress]",
                response_time=total_time,
                response_length=len(response.terms),
                exception=None,
                context={}
            )
        except Exception as e:
            total_time = int((time.time() - start_time) * 1000)
            events.request.fire(
                request_type="grpc",
                name="SearchTerms [stress]",
                response_time=total_time,
                response_length=0,
                exception=e,
                context={}
            )
    
    @task(20)
    def rapid_get(self):
        """Rapid get requests"""
        start_time = time.time()
        try:
            term_id = random.choice(['grpc', 'protobuf', 'http2', 'rpc', 'api', 'rest'])
            request = glossary_pb2.GetTermRequest(term_id=term_id)
            response = self.client.stub.GetTerm(request, timeout=5)
            
            total_time = int((time.time() - start_time) * 1000)
            events.request.fire(
                request_type="grpc",
                name="GetTerm [stress]",
                response_time=total_time,
                response_length=1,
                exception=None,
                context={}
            )
        except Exception as e:
            total_time = int((time.time() - start_time) * 1000)
            events.request.fire(
                request_type="grpc",
                name="GetTerm [stress]",
                response_time=total_time,
                response_length=0,
                exception=e,
                context={}
            )

