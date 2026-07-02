"use client";
import { useState, useEffect } from "react";
import SearchBar from "@/components/SearchBar";
import FacetSidebar from "@/components/FacetSidebar";
import SearchResults from "@/components/SearchResults";
import IndexStats from "@/components/IndexStats";
import { searchProducts, getFacets, rebuildIndex } from "@/lib/api";

export default function Home() {
  const [query, setQuery] = useState("");
  const [filters, setFilters] = useState<Record<string,string>>({});
  const [results, setResults] = useState<any>(null);
  const [facets, setFacets] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const handleSearch = async (q: string, f: Record<string,string> = filters) => {
    setLoading(true);
    const [res, fac] = await Promise.all([
      searchProducts({ q, ...f }),
      getFacets(q),
    ]);
    setResults(res);
    setFacets(fac);
    setLoading(false);
  };

  useEffect(() => { handleSearch(""); }, []);

  return (
    <div className="min-h-screen bg-gray-950 text-gray-100">
      <header className="border-b border-gray-800 px-6 py-4">
        <h1 className="text-2xl font-bold text-indigo-400">Product Index Builder</h1>
        <IndexStats />
      </header>
      <div className="px-6 py-4">
        <SearchBar query={query} onChange={setQuery} onSearch={() => handleSearch(query)} />
      </div>
      <div className="flex px-6 gap-6">
        <aside className="w-64 shrink-0">
          <FacetSidebar facets={facets} onFilter={(f) => { setFilters(f); handleSearch(query, f); }} />
        </aside>
        <main className="flex-1">
          <SearchResults results={results} loading={loading} />
        </main>
      </div>
    </div>
  );
}